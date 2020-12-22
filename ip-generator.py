for i in range(6,100):
  ip = "192.168.1." + str(i)
  hostname = 'vm' + str(i)
  ipl = Ipinfo(ip=ip, hostname=hostname, device_type='vm', user='xiao', project='uat')
  db.session.add(ipl)
  db.session.commit()
