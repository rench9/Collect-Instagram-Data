## code 1 = start, 0 = stop, 2 = pause
import threading


# timeSeries = 0  # 1
# usersInfo = 0  # 2
# usersInfoSingle = 0  # 3
# followersSingle = 0  # 4
# usersInfoMass = 0  # 5
# postsMass = 0  # 6
# importCSV = 0  # 7

# _isRunning = False

class _s():
    def __init__(self):
        super(_s, self).__init__()
        self._start_event = threading.Event()
        # self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        pass

    def start(self):
        self._start_event.set()

    def started(self):
        return self._start_event.is_set()

    def stop(self):
        self._start_event.clear()
        # self._stop_event.set()

    # def stopped(self):
    #     return self._stop_event.is_set()

    def pause(self):
        self._pause_event.set()

    def paused(self):
        return self._pause_event.is_set()

    def resume(self):
        self._pause_event.clear()

    pass


timeSeries = _s()
usersInfo = _s()
usersInfoSingle = _s()
followersSingle = _s()
usersInfoMass = _s()
postsMass = _s()
importCSV = _s()

main = _s()

# def start(taskCode):
#     global timeSeries
#     global usersInfo
#     global usersInfoSingle
#     global followersSingle
#     global usersInfoMass
#     global postsMass
#     global importCSV
#     if taskCode == 1:
#         if usersInfo == 1:
#             usersInfo == 2
#         if usersInfoSingle == 1:
#             usersInfoSingle == 2
#         if followersSingle == 1:
#             followersSingle == 2
#         if usersInfoMass == 1:
#             usersInfoMass == 2
#         if postsMass == 1:
#             postsMass == 2
#         if importCSV == 1:
#             importCSV == 2
#         timeSeries = 1
#         pass
#     elif taskCode == 2:
#         if timeSeries == 1:
#             timeSeries == 2
#         if usersInfoSingle == 1:
#             usersInfoSingle == 2
#         if followersSingle == 1:
#             followersSingle == 2
#         if usersInfoMass == 1:
#             usersInfoMass == 2
#         if postsMass == 1:
#             postsMass == 2
#         if importCSV == 1:
#             importCSV == 2
#         usersInfo = 1
#         pass
#     elif taskCode == 3:
#         if timeSeries == 1:
#             timeSeries == 2
#         if usersInfo == 1:
#             usersInfo == 2
#         if followersSingle == 1:
#             followersSingle == 2
#         if usersInfoMass == 1:
#             usersInfoMass == 2
#         if postsMass == 1:
#             postsMass == 2
#         if importCSV == 1:
#             importCSV == 2
#         usersInfoSingle = 1
#         pass
#     elif taskCode == 4:
#         if timeSeries == 1:
#             timeSeries == 2
#         if usersInfo == 1:
#             usersInfo == 2
#         if usersInfoSingle == 1:
#             usersInfoSingle == 2
#         if usersInfoMass == 1:
#             usersInfoMass == 2
#         if postsMass == 1:
#             postsMass == 2
#         if importCSV == 1:
#             importCSV == 2
#         followersSingle = 1
#         pass
#     elif taskCode == 5:
#         if timeSeries == 1:
#             timeSeries == 2
#         if usersInfo == 1:
#             usersInfo == 2
#         if usersInfoSingle == 1:
#             usersInfoSingle == 2
#         if followersSingle == 1:
#             followersSingle == 2
#         if postsMass == 1:
#             postsMass == 2
#         if importCSV == 1:
#             importCSV == 2
#         usersInfoMass = 1
#         pass
#     elif taskCode == 6:
#         if timeSeries == 1:
#             timeSeries == 2
#         if usersInfo == 1:
#             usersInfo == 2
#         if usersInfoSingle == 1:
#             usersInfoSingle == 2
#         if followersSingle == 1:
#             followersSingle == 2
#         if usersInfoMass == 1:
#             usersInfoMass == 2
#         if importCSV == 1:
#             importCSV == 2
#         postsMass = 1
#         pass
#     elif taskCode == 7:
#         if timeSeries == 1:
#             timeSeries == 2
#         if usersInfo == 1:
#             usersInfo == 2
#         if usersInfoSingle == 1:
#             usersInfoSingle == 2
#         if followersSingle == 1:
#             followersSingle == 2
#         if usersInfoMass == 1:
#             usersInfoMass == 2
#         if postsMass == 1:
#             postsMass == 2
#         importCSV = 1
#         pass
#     pass
#
#
# def stop(taskCode):
#     global timeSeries
#     global usersInfo
#     global usersInfoSingle
#     global followersSingle
#     global usersInfoMass
#     global postsMass
#     global importCSV
#     if taskCode == 1:
#         timeSeries = 0
#         pass
#     elif taskCode == 2:
#         usersInfo = 0
#         pass
#     elif taskCode == 3:
#         usersInfoSingle = 0
#         pass
#     elif taskCode == 4:
#         followersSingle = 0
#         pass
#     elif taskCode == 5:
#         usersInfoMass = 0
#         pass
#     elif taskCode == 6:
#         postsMass = 0
#         pass
#     elif taskCode == 7:
#         importCSV = 0
#         pass
#     pass
#
#
# def pause(taskCode):
#     global timeSeries
#     global usersInfo
#     global usersInfoSingle
#     global followersSingle
#     global usersInfoMass
#     global postsMass
#     global importCSV
#     if taskCode == 1:
#         timeSeries = 2
#         pass
#     elif taskCode == 2:
#         usersInfo = 2
#         pass
#     elif taskCode == 3:
#         usersInfoSingle = 2
#         pass
#     elif taskCode == 4:
#         followersSingle = 2
#         pass
#     elif taskCode == 5:
#         usersInfoMass = 2
#         pass
#     elif taskCode == 6:
#         postsMass = 2
#         pass
#     elif taskCode == 7:
#         importCSV = 2
#         pass
#     pass
