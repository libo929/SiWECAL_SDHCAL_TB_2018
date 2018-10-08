from DDSim.DD4hepSimulation import DD4hepSimulation
from SystemOfUnits import mm, GeV, MeV

SIM = DD4hepSimulation()

SIM.runType = "batch"
SIM.numberOfEvents = 3

SIM.skipNEvents = 0
SIM.outputFile = "gun_test.slcio"

SIM.compactFile = "MainSetup.xml"
SIM.dumpSteeringFile = "dumpSteering.xml"

SIM.field.eps_min = 1*mm
SIM.part.minimalKineticEnergy = 1*MeV
SIM.physicsList = "QGSP_BERT"
SIM.enableDetailedShowerMode=True

SIM.enableGun = True
SIM.gun.energy = 10*GeV
SIM.gun.particle = "mu-"
SIM.gun.position = "0,70,-1000"
SIM.gun.direction = "0,0,1"
