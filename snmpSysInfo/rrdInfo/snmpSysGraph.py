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

    createCpuGraph()
    createRamGraph()
    createDiskGraph()


def createCpuGraph():
    tmp = time()

    try:
        rrdtool.graph(
            "./graph/cpuGraph" + str(tmp) + ".png",
            "--width", "1600",
            "--height", "400",
            "--start", "now-1hour",
            "--end","now",
            "--lower-limit", "0",
            "--upper-limit", "100",
            "--title", "Cpu Usage Percentage",
            "--vertical-label", "CPU %",
            "DEF:cpu=./rrdLogs/cpu.rrd:cpu:AVERAGE",
            "VDEF:msmax=cpu,MAXIMUM",
            "VDEF:msavg=cpu,AVERAGE",
            "VDEF:msmin=cpu,MINIMUM",
            "LINE1:cpu#ff0000:CPU",
            r"GPRINT:msmax:Max\: %6.1lf %%",
            r"GPRINT:msavg:Avg\: %6.1lf %%",
            r"GPRINT:msmin:Min\: %6.1lf %%",
        )
    except:
        print("ERROR: Problem while creating the CPU Graph, program will now terminate.")
        exit(1)

def createRamGraph():
    tmp = time()

    try:
        rrdtool.graph(
            "./graph/ramGraph" + str(tmp) + ".png",
            "--width", "1600",
            "--height", "400",
            "--start", "now-1hour",
            "--end","now",
            #"--lower-limit", "0",
            #"--upper-limit", "100",
            "--title", "Ram Usage Bytes",
            "--vertical-label", "RAM Bytes",
            "DEF:ram=./rrdLogs/ram.rrd:ram:AVERAGE",
            "CDEF:mram=ram,1024,/",
            "CDEF:gram=mram,1024,/",
            "VDEF:bmmax=ram,MAXIMUM",
            "VDEF:mmmax=mram,MAXIMUM",
            "VDEF:gmmax=gram,MAXIMUM",
            "VDEF:baavg=ram,AVERAGE",
            "VDEF:maavg=mram,AVERAGE",
            "VDEF:gaavg=gram,AVERAGE",
            "VDEF:bmmmin=ram,MINIMUM",
            "VDEF:mmmmin=mram,MINIMUM",
            "VDEF:gmmmin=gram,MINIMUM",
            "LINE1:ram#ff0000:RAM",
            r"GPRINT:bmmax:Max\: %6.1lf B",
            r"GPRINT:mmmax:Max\: %6.1lf MB",
            r"GPRINT:gmmax:Max\: %6.1lf GB",
            r"GPRINT:baavg:Avg\: %6.1lf B",
            r"GPRINT:maavg:Avg\: %6.1lf MB",
            r"GPRINT:gaavg:Avg\: %6.1lf GB",
            r"GPRINT:bmmmin:Min\: %6.1lf B",
            r"GPRINT:mmmmin:Min\: %6.1lf MB",
            r"GPRINT:gmmmin:Min\: %6.1lf GB",
        )
    except:
        print("ERROR: Problem while creating the RAM Graph, program will now terminate.")
        exit(1)

def createDiskGraph():
    tmp = time()

    try:
        rrdtool.graph(
            "./graph/diskGraph" + str(tmp) + ".png",
            "--width", "1600",
            "--height", "400",
            "--start", "now-1hour",
            "--end","now",
            "--lower-limit", "0",
            "--upper-limit", "100",
            "--title", "Disk Usage Percentage",
            "--vertical-label", "DISK %",
            "DEF:in=./rrdLogs/disk.rrd:disk:AVERAGE",
            "VDEF:msmax=in,MAXIMUM",
            "VDEF:msavg=in,AVERAGE",
            "VDEF:msmin=in,MINIMUM",
            "LINE1:in#ff0000:DISK",
            r"GPRINT:msmax:Max\: %6.1lf %%",
            r"GPRINT:msavg:Avg\: %6.1lf %%",
            r"GPRINT:msmin:Min\: %6.1lf %%",
        )
    except:
        print("ERROR: Problem while creating the DISK Graph, program will now terminate.")
        exit(1)


def main():

    createDirGraph()


main()