from dashboard.models import Logs


def writeLog(code, title, desc):
    log = Logs.objects.create()
    log.title = title
    log.code = code
    log.desc = desc
    log.save()

    # def writeLog(self):
    #     log = Logs.objects.create()
    #     log.title = self.title
    #     log.code = self.code
    #     log.desc = self.desc
    #     log.save()
