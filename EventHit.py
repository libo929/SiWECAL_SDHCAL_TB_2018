
#ROOT
import ROOT
from ROOT import TCanvas
from ROOT import TGraph
from ROOT import gROOT
from ROOT import TLegend
from ROOT import TFile
from ROOT import TGaxis
from ROOT import gDirectory
from ROOT import gStyle
from ROOT import gPad
from ROOT import TH1F
from ROOT import TF1
from ROOT import TVector3
from ROOT import TEveEventManager
from ROOT import TNtupleD

# LCIO
from pyLCIO.io.LcioReader import LcioReader
from pyLCIO.io.Reader import Reader
from pyLCIO import EVENT
from pyLCIO import UTIL

import sys

#########################################

class EventReader:
    def __init__(self, fileName) :
        self._lcioReader = LcioReader( fileName )
        self._event = None

    def readEvent(self):
        
        runNumber = self._lcioReader.getNumberOfRuns()

        try:
              self._event = self._lcioReader.next()
        except:
              return None

        evtNum = self._event.getEventNumber()

        pfoTargetCandidates = []

        hits = self._event.getCollection('SDHcalCollection')
        nHits = hits.getNumberOfElements()
        cellIdEncoding = hits.getParameters().getStringVal( EVENT.LCIO.CellIDEncoding )
        idDecoder = UTIL.BitField64( cellIdEncoding )

        print 'Event : ', evtNum, ', # of SDHCAL hits: ', nHits

        hitsLayer = []

        for iHit in range(0, nHits):
            hit = hits.getElementAt( iHit )
            cellID = long( hit.getCellID0() & 0xffffffff ) | ( long( hit.getCellID1() ) << 32 )
            idDecoder.setValue( cellID )
            layer = int( idDecoder['K'].value() )
            hitsLayer.append( layer )

            #print 'hit layer: %d' % (layer)

        return self._event, hitsLayer


if __name__=='__main__':
    if len(sys.argv) == 4:
        fileName = sys.argv[1]
        minClusterSize = int(sys.argv[2])
        maxClusterSize = int(sys.argv[3])
		
        if minClusterSize > maxClusterSize:
            minClusterSize, maxClusterSize = maxClusterSize, minClusterSize
	
    if len(sys.argv) == 2:
        fileName = sys.argv[1]
	
    if len(sys.argv) == 1:
        fileName = 'teve_infile.slcio'

    eventNumber = 1
    print 'Loaded file: ', fileName
    er = EventReader( fileName )

    event = None
    #maxEvent = 3
    maxEvent = 2000
    iEvent = 0

    hist = TH1F('', '', 20, 0, 20)

    while True:
         event, hitsLayer = er.readEvent()
         #print hitsLayer
         for layer in hitsLayer:
             hist.Fill( layer )

         if event == None or iEvent >= maxEvent-1:
             break

         iEvent = iEvent + 1

    canvas = TCanvas('can', 'can', 600, 600)
    #canvas.SetLogy()
    histIntergal = hist.Integral()
    hist.Scale(1./histIntergal)
    #hist.Fit("expo")
    hist.GetXaxis().SetTitle('Layer')
    hist.GetYaxis().SetTitle('Hit probability')
    hist.GetYaxis().SetTitleOffset(1.45)
    hist.SetLineWidth( 3 )
    hist.SetLineColor( 6 ) # Pink
    gStyle.SetOptStat(000)
    hist.Draw()
    canvas.Print('Hitlayer.pdf')
