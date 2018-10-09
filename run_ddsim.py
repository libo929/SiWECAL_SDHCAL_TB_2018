from DDSim.DD4hepSimulation import DD4hepSimulation
from SystemOfUnits import mm, GeV, MeV

SIM = DD4hepSimulation()

SIM.runType = "batch"
#SIM.numberOfEvents = 2000
SIM.numberOfEvents = 20

SIM.skipNEvents = 0
SIM.outputFile = "gun_test.slcio"

SIM.compactFile = "MainSetup.xml"
SIM.dumpSteeringFile = "dumpSteering.xml"

SIM.field.eps_min = 1*mm
SIM.part.minimalKineticEnergy = 1*MeV
SIM.physicsList = "QGSP_BERT"
SIM.enableDetailedShowerMode=True

SIM.enableGun = True
SIM.gun.energy = 80*GeV
SIM.gun.particle = "e-"
#SIM.gun.position = "184.+88., -32.-88., -10" # bottom left corner of ECAL
SIM.gun.position = "184., -32., -1." # center of ECAL
SIM.gun.direction = "0,0,1"
