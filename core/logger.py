# -*- coding: utf-8 -*-
import time

class LogEntry:
    def __init__(self, timestamp, type_, message):
        self.timestamp = timestamp
        self.type_ = type_ # "info", "warning", "error", "connection", "pid"
        self.message = message

class AppLogger:
    def __init__(self):
        self.entries = []

    def log(self, type_, message):
        self.entries.append(LogEntry(time.time(), type_, message))

    def clear(self):
        del self.entries[:]

logger = AppLogger()
