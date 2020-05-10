from threading import Thread
from holt_winters import triple_exponential_smoothing
from time import time
from time import sleep
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS


class Sender(Thread):
    def __init__(self, write_api, db_bucket, agent_loc, inOctets, inOctetsTime, outOctets, outOctetsTime):
        super().__init__()
        self.write_api = write_api
        self.db_bucket = db_bucket
        self.agent_loc = agent_loc
        self.lastIn = 0
        self.lastOut = 0
        self.start_time = 0
        self.season_lenght = 12
        self.alpha = 0.9
        self.beta = 0.9
        self.gamma = 0.9
        self.num_values_to_predict = 0
        self.inOctets = inOctets
        self.inOctetsTime = inOctetsTime
        self.outOctets = outOctets
        self.outOctetsTime = outOctetsTime

    # Function that add values to the influx DB
    def sendValue(self):
        self.start_time = time()

        if(self.inOctets is None or self.outOctets is None):
            return

        tmp_in = len(self.inOctets)
        tmp_out = len(self.outOctets)

        print(tmp_in)

        if(tmp_in < 24 or tmp_in - self.lastIn < 12):
            if(tmp_in > 0):
                print(type(self.inOctets[0]))
            intes, indeviation = [], []

        else:
            intes, indeviation = triple_exponential_smoothing(self.inOctets, tmp_in, self.season_lenght, self.alpha,
                                                              self.beta, self.gamma,
                                                              self.num_values_to_predict)

        if(tmp_out < 24 or tmp_out - self.lastOut < 12):
            outtes, outdeviation = [], []

        else:
            outtes, outdeviation = triple_exponential_smoothing(self.outOctets, tmp_out, self.season_lenght, self.alpha,
                                                                self.beta, self.gamma,
                                                                self.num_values_to_predict)


        try:
            print(self.inOctets)
            if len(intes) != 0:
                value_list = []

                lenght = self.lastIn - tmp_in

                for i in range(self.lastIn, tmp_in):
                    # InOctets
                    #   valuespoint = Point("mem")\
                    #   .tag("host", "host1")\
                    #   .field("used_percent", 23.43234543)\
                    #   .time(1556896326, WritePrecision.NS)
                    value_list.append(Point("inOctetsHW").tag("location", self.agent_loc).field("hw", int(intes[i % lenght]))
                                                                                                .time(self.inOctetsTime[i], WritePrecision.NS))
                    value_list.append(Point("inOctetsHW").tag("location", self.agent_loc).field("deviationUp",
                                                                                                int(intes[i % lenght] + indeviation[i % lenght]))
                                                                                                .time(self.inOctetsTime[i], WritePrecision.NS))
                    value_list.append(Point("inOctetsHW").tag("location", self.agent_loc).field("deviationDown",
                                                                                                int(intes[i % lenght] - indeviation[i % lenght]))
                                                                                                .time(self.inOctetsTime[i], WritePrecision.NS))
                    value_list.append(Point("inOctetsHW").tag("location", self.agent_loc).field("octets",
                                                                                                int(self.inOctets[i]))
                                                                                                .time(self.inOctetsTime[i], WritePrecision.NS))
                    #value_list.append('inOctetsHW,location=' + self.agent_loc + ' hw=' + str(intes[i]))
                    #value_list.append('inOctetsHW,location=' + self.agent_loc + ' deviationUp=' + str(intes[i] + indeviation[i]))
                    #value_list.append('inOctetsHW,location=' + self.agent_loc + ' deviationDown=' + str(intes[i] - indeviation[i]))
                    #value_list.append('inOctetsHW,location=' + self.agent_loc + ' octets=' + str(self.inOctets[i]))

                print(value_list)

                for i in range(len(value_list)):
                    self.write_api.write(bucket=self.db_bucket, record=value_list[i])

                self.lastIn = tmp_in



            # OutOctets values
            print(self.outOctets)
            if len(outtes) != 0:
                value_list = []

                lenght = self.lastOut - tmp_out

                for i in range(self.lastOut, tmp_out):
                    # InOctets values
                    value_list.append(Point("outOctetsHW").tag("location", self.agent_loc).field("hw", int(outtes[i % lenght]))
                                                                                                .time(self.outOctetsTime[
                                                                                                          i],
                                                                                                      WritePrecision.NS))
                    value_list.append(Point("outOctetsHW").tag("location", self.agent_loc).field("deviationUp",
                                                                                                int(outtes[i % lenght] +
                                                                                                    outdeviation[i % lenght]))
                                                                                                .time(self.outOctetsTime[
                                                                                                          i],
                                                                                                      WritePrecision.NS))
                    value_list.append(Point("outOctetsHW").tag("location", self.agent_loc).field("deviationDown",
                                                                                                int(outtes[i % lenght] -
                                                                                                    outdeviation[i % lenght]))
                                                                                                .time(self.outOctetsTime[
                                                                                                          i],
                                                                                                      WritePrecision.NS))
                    value_list.append(Point("outOctetsHW").tag("location", self.agent_loc).field("octets",
                                                                                                int(self.outOctets[i]))
                                                                                                .time(self.outOctetsTime[
                                                                                                          i],
                                                                                                      WritePrecision.NS))
                    #value_list.append('outOctetsHW,location=' + self.agent_loc + ' hw=' + str(outtes[i]))
                    #value_list.append('outOctetsHW,location=' + self.agent_loc + ' deviationUp=' + str(outtes[i] + outdeviation[i]))
                    #value_list.append('outOctetsHW,location=' + self.agent_loc + ' deviationDown=' + str(outtes[i] - outdeviation[i]))
                    #value_list.append('outOctetsHW,location=' + self.agent_loc + ' octets=' + str(self.outOctets[i]))

                print(value_list)
                for i in range(len(value_list)):
                    self.write_api.write(bucket=self.db_bucket, record=value_list[i])

                self.lastOut = tmp_out



        except KeyboardInterrupt:
            exit(1)

        #except:
        #    print('ERROR: while adding values to the database, check bucket name (-b option)')
        #   exit(1)


    # Function to let the program sleep at max for 5 sec
    def sleep_fun(self):
        sleepTime = time() - self.start_time

        if sleepTime < 60:
            sleepTime = 60 - sleepTime

            try:
                sleep(sleepTime)
            except KeyboardInterrupt:
                exit(1)


    def run(self):
        while(True):
            self.sendValue()
            self.sleep_fun()