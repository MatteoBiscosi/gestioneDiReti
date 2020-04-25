#!/usr/bin/python3

# Import
import rrdtool
import os.path
from time import time


def createDirGraph():
    if not os.path.isdir("./graph"):
        try:
            os.mkdir("./graph")
        except:
            print("ERROR: Problem while creating the directory, program will now terminate.")
            exit(1)

    createInGraph()
    createOutGraph()


def createInGraph():
    tmp = str(time())

    tmp = tmp.replace(".", "")

    try:
        rrdtool.graph(
            "./graph/inOctetGraph" + tmp + ".png",
            "--width", "1600",
            "--height", "400",
            "--start", "now-1hour",
            "--end","now",
            "--title", "InOctets",
            "--vertical-label", "Bytes",
            "DEF:inOctet=./rrdLogs/inOctet.rrd:inOctet:AVERAGE",
            "DEF:pred=./rrdLogs/inOctet.rrd:inOctet:HWPREDICT",
            "DEF:dev=./rrdLogs/inOctet.rrd:inOctet:DEVPREDICT",
            "DEF:fail=./rrdLogs/inOctet.rrd:inOctet:FAILURES",
            "TICK:fail#ffffa0:1.0:Failures Average bits out",
            "CDEF:upper=pred,dev,2,*,+",
            "CDEF:lower=pred,dev,2,*,-",
            "CDEF:scaledupper=upper,8,*",
            "CDEF:scaledlower=lower,8,*",
            "VDEF:msmax=inOctet,MAXIMUM",
            "VDEF:msavg=inOctet,AVERAGE",
            "VDEF:msmin=inOctet,MINIMUM",
            "LINE2:inOctet#0000ff:InOctet",
            "LINE1:scaledupper#ff0000:Upper Bound Average bits out",
            "LINE1:scaledlower#ff0000:Lower Bound Average bits out",
            r"GPRINT:msmax:Max\: %6.1lf Bytes",
            r"GPRINT:msavg:Avg\: %6.1lf Bytes",
            r"GPRINT:msmin:Min\: %6.1lf Bytes",
        )
    except:
        print("ERROR: Problem while creating the CPU Graph, program will now terminate.")
        exit(1)


def createOutGraph():
    tmp = str(time())

    tmp = tmp.replace(".", "")

    try:
        rrdtool.graph(
            "./graph/ramGraph" + tmp + ".png",
            "--width", "1600",
            "--height", "400",
            "--start", "now-1hour",
            "--end","now",
            "--title", "OutOctet Bytes",
            "--vertical-label", "RAM Bytes",
            "DEF:outOctet=./rrdLogs/outOctet.rrd:outOctet:AVERAGE",
            "DEF:pred=./rrdLogs/outOctet.rrd:outOctet:HWPREDICT",
            "DEF:dev=./rrdLogs/outOctet.rrd:outOctet:DEVPREDICT",
            "DEF:fail=./rrdLogs/outOctet.rrd:outOctet:FAILURES",
            "TICK:fail#ffffa0:1.0:Failures Average bits out",
            "CDEF:upper=pred,dev,2,*,+",
            "CDEF:lower=pred,dev,2,*,-",
            "CDEF:scaledupper=upper,8,*",
            "CDEF:scaledlower=lower,8,*",
            "VDEF:msmax=outOctet,MAXIMUM",
            "VDEF:msavg=outOctet,AVERAGE",
            "VDEF:msmin=outOctet,MINIMUM",
            "LINE2:outOctet#0000ff:InOctet",
            "LINE1:scaledupper#ff0000:Upper Bound Average bits out",
            "LINE1:scaledlower#ff0000:Lower Bound Average bits out",
            r"GPRINT:msmax:Max\: %6.1lf Bytes",
            r"GPRINT:msavg:Avg\: %6.1lf Bytes",
            r"GPRINT:msmin:Min\: %6.1lf Bytes",
        )
    except:
        print("ERROR: Problem while creating the RAM Graph, program will now terminate.")
        exit(1)


def main():

    createDirGraph()


main()