import ROOT as rt
from math import isinf
from math import acos
rt.TH1F.SetDefaultSumw2(rt.kTRUE)
rt.gStyle.SetOptStat(0)




inFile1 = rt.TFile("dlgen2_reco_v2me06_ntuple_v5_mcc9_v28_wctagger_nueintrinsics.root")
inFile2 = rt.TFile("dlgen2_reco_v2me06_ntuple_v5_mcc9_v28_wctagger_bnboverlay.root")
inFile3 = rt.TFile("prepare_selection_test_reco_v2me05_gen2val_v22_extbnb_file.root")
tree1 = inFile1.Get("EventTree")
tree2 = inFile2.Get("EventTree")
tree3 = inFile3.Get("EventTree")
potTree1 = inFile1.Get("potTree")
potTree2 = inFile2.Get("potTree")


totPot1 = 0 ########Change this BACK###
dataPot1 = 6.67e20
for i in range(potTree1.GetEntries()):
	potTree1.GetEntry(i)
	totPot1 += potTree1.totGoodPOT

totPot2 = 0
dataPot2 = 6.67e20
for i in range(potTree2.GetEntries()):
        potTree2.GetEntry(i)
        totPot2 += potTree2.totGoodPOT

totPot = totPot1 + totPot2
dataPot = 6.67e20

totPot3 = 4.79e19
dataPot3 = 6.67e20

scale1 = dataPot1/totPot1
scale2 = dataPot2/totPot2
scale3 = dataPot3/totPot3


#creating all the histograms
CCeTrue = rt.TH1F("CCe", "True NuE for True MiniBoone Events", 100, 0, 5)
NCeTrue = rt.TH1F("NCe", "True NuE for True MiniBoone Events", 100, 0, 5)
CCmTrue = rt.TH1F("CCm", "True NuE for True MiniBoone Events", 100, 0, 5)
NCmTrue = rt.TH1F("NCm", "True NuE for True MiniBoone Events", 100, 0, 5)

CCeTrueReco = rt.TH1F("CCeTR", "True NuE for Reconstructed & True MiniBoone Events", 100, 0, 5)
NCeTrueReco = rt.TH1F("NCeTR", "True NuE for Reconstructed & True MiniBoone Events", 100, 0, 5)
CCmTrueReco = rt.TH1F("CCmTR", "True NuE for Reconstructed & True MiniBoone Events", 100, 0, 5)
NCmTrueReco = rt.TH1F("NCmTR", "True NuE for Reconstructed & True MiniBoone Events", 100, 0, 5)

recoTruePurityCCe = rt.TH1F("rtpurityCCe ", "Reco NuE for Reco and True MiniBooNE Events", 30, 0, 3000)
recoTruePurityNCe = rt.TH1F("rtpurityNCe ", "Reco NuE for Reco and True MiniBooNE Events", 30, 0, 3000)
recoTruePurityCCm = rt.TH1F("rtpurityCCm ", "Reco NuE for Reco and True MiniBooNE Events", 30, 0, 3000)
recoTruePurityNCm = rt.TH1F("rtpurityNCm ", "Reco NuE for Reco and True MiniBooNE Events", 30, 0, 3000)

recoPurityCCe = rt.TH1F("purityCCe", "Reco NuE for Reco MiniBooNE Events", 30, 0, 3000)
recoPurityNCe = rt.TH1F("purityNCe", "Reco NuE for Reco MiniBooNE Events", 30, 0, 3000)
recoPurityCCm = rt.TH1F("purityCCm", "Reco NuE for Reco MiniBooNE Events", 30, 0, 3000)
recoPurityNCm = rt.TH1F("purityNCm", "Reco NuE for Reco MiniBooNE Events", 30, 0, 3000)
recoPurityCB = rt.TH1F("purityCB", "Reco NuE for Reco MiniBooNE Events", 30, 0, 3000)



TrueAndRecoEvents = 0
TrueEvents = 0
RecoEvents = 0


#Filling from tree 2
for i in range (tree2.GetEntries()):
#for i in range (5000):
			ShowerPDG = 0
			tree2.GetEntry(i)
			showerCount = 0
			pionCount = 0 
			muonCount = 0 
			protonCount = 0
			NpionCount = 0
			TrueEvent = "True"
			RecoEvent = "True"
			if isinf (tree2.xsecWeight):
                                continue

			#Testing if it is a true event
			for p in range (tree2.nTrueSimParts):
				if tree2.trueSimPartProcess[p] !=0:
					continue				
				detCrds = [[0., 256.35], [-116.5, 116.5], [0, 1036.8]] #256.35, 116.5, 1036.8
				def inRange(x, bound):
					return (x >= bound[0] and x <= bound[1])
				def isInDetector(X,Y,Z):
					return (inRange(X, detCrds[0]), inRange(Y,detCrds[1]), inRange(Z,detCrds[2]))
				if tree2.trueSimPartPDG[p] == 22:
					PhotoninDetector = False
					if isInDetector(tree2.trueSimPartEDepX[p],tree2.trueSimPartEDepY[p], tree2.trueSimPartEDepZ[p]) == (True, True, True):
						#p energy is in detector
						PhotoninDetector = True
					if PhotoninDetector == True:
						showerCount += 1
				if tree2.trueSimPartPDG[p] == 11 or tree2.trueSimPartPDG[p] == -11:
					ElectronInDetector = False
					if isInDetector(tree2.trueSimPartEDepX[p],tree2.trueSimPartEDepY[p], tree2.trueSimPartEDepZ[p]) == (True, True, True):
						#e is in detector
						ElectronInDetector = True
					if ElectronInDetector == True:
						showerCount += 1
				if tree2.trueSimPartPDG[p] == 13 or tree2.trueSimPartPDG[p] == -13:
					if tree2.trueSimPartE[p] > 144.3:
						muonCount += 1
				if tree2.trueSimPartPDG[p] == 211 or tree2.trueSimPartPDG[p] == -211:
					if tree2.trueSimPartE[p] > 190.6:
						pionCount += 1
				if tree2.trueSimPartPDG[p] == 2212 or tree2.trueSimPartPDG[p] == -2212:
					if tree2.trueSimPartE[p] > 1288.3:
						protonCount += 1
			
			for p in range (tree2.nTruePrimParts):
				if tree2.truePrimPartPDG[p] == 111:
					NpionCount += 1
			if showerCount != 1:
				TrueEvent = "False"
			if muonCount != 0 or protonCount != 0 or pionCount != 0 or NpionCount != 0:
				TrueEvent = "False"
		
			#testing if it is a reco event
			primCompShowers = 0
			for s in range(tree2.nShowers):
				if tree2.showerClassified[s] == 1 and tree2.showerComp[s] > 0.4:
					if tree2.showerPID[s] != 22 and tree2.showerPID[s] != 11 and tree2.showerPID[s] != -11:
						RecoEvent = "False"
						continue
					ElPhmPiScore = 0 
					if tree2.showerElScore[s] >= tree2.showerPhScore[s]:
						ElPhmPiScore = tree2.showerElScore[s] - tree2.showerPiScore[s]
					if tree2.showerPhScore[s] > tree2.showerElScore[s]:
						ElPhmPiScore = tree2.showerPhScore[s] - tree2.showerPiScore[s]

					if ElPhmPiScore < 10.3:
						RecoEvent = "False"
						continue
					primCompShowers += 1
			if primCompShowers != 1:
				RecoEvent = "False"
			if tree2.foundVertex != 1:
				RecoEvent = "False"
			if tree2.vtxIsFiducial != 1:
				RecoEvent = "False"
			if tree2.vtxFracHitsOnCosmic >= 1:
				RecoEvent = "False"
			for t in range(tree2.nTracks):
				if tree2.trackIsSecondary[t] == 1 or tree2.trackClassified[t] !=1:
					continue
				if tree2.trackPID[t] == 211: #pions
					if tree2.trackRecoE[t] >= 51.0:
						RecoEvent = "False"
				if tree2.trackPID[t] == 13: #muons
					if tree2.trackRecoE[t] >= 38.6:
						RecoEvent = "False"
				if tree2.trackPID[t] == 2212: #protons
					if tree2.trackRecoE[t] >= 350:
						RecoEvent = "False"
			

			
			#filling histograms correctly
			if TrueEvent == "True":
				if tree2.trueNuCCNC == 0 and tree2.trueNuPDG == 14: #CCm
					CCmTrue.Fill(tree2.trueNuE, tree2.xsecWeight)
					TrueEvents += tree2.xsecWeight*scale2
				if tree2.trueNuCCNC == 1 and tree2.trueNuPDG == 14: #NCm
					NCmTrue.Fill(tree2.trueNuE, tree2.xsecWeight)
					TrueEvents += tree2.xsecWeight*scale2
				if tree2.trueNuCCNC == 1 and tree2.trueNuPDG == 12: #NCe
					NCeTrue.Fill(tree2.trueNuE, tree2.xsecWeight)
					TrueEvents += tree2.xsecWeight*scale2

			if TrueEvent == "True" and RecoEvent == "True":  #signal events
				if tree2.trueNuCCNC == 0 and tree2.trueNuPDG == 14: #CCm
					CCmTrueReco.Fill(tree2.trueNuE, tree2.xsecWeight)
					recoTruePurityCCm.Fill(tree2.recoNuE, tree2.xsecWeight)
					TrueAndRecoEvents += tree2.xsecWeight*scale2
				if tree2.trueNuCCNC == 1 and tree2.trueNuPDG == 14: #NCm 
					NCmTrueReco.Fill(tree2.trueNuE, tree2.xsecWeight)
					recoTruePurityNCm.Fill(tree2.recoNuE, tree2.xsecWeight)
					TrueAndRecoEvents += tree2.xsecWeight*scale2
				if tree2.trueNuCCNC == 1 and tree2.trueNuPDG == 12: #NCe 
					NCeTrueReco.Fill(tree2.trueNuE, tree2.xsecWeight)
					recoTruePurityNCe.Fill(tree2.recoNuE, tree2.xsecWeight)
					TrueAndRecoEvents += tree2.xsecWeight*scale2
			
			if RecoEvent == "True":
				if tree2.trueNuCCNC == 0 and tree2.trueNuPDG == 14: #CCm
					recoPurityCCm.Fill(tree2.recoNuE, tree2.xsecWeight)
					RecoEvents += tree2.xsecWeight*scale2
				if tree2.trueNuCCNC == 1 and tree2.trueNuPDG == 14: #NCm
					recoPurityNCm.Fill(tree2.recoNuE, tree2.xsecWeight)
					RecoEvents += tree2.xsecWeight*scale2
				if tree2.trueNuCCNC == 1 and tree2.trueNuPDG == 12: #NCe
					recoPurityNCe.Fill(tree2.recoNuE, tree2.xsecWeight)
					RecoEvents += tree2.xsecWeight*scale2
			#if RecoEvent == "True" and TrueEvent != "True": #background events
						


#Filling from tree 1
for i in range (tree1.GetEntries()):
#for i in range (5000):
			ShowerPDG = 0
			tree1.GetEntry(i)
			showerCount = 0
			pionCount = 0 
			muonCount = 0 
			protonCount = 0
			NpionCount = 0
			TrueEvent = "True"
			RecoEvent = "True"
			if isinf (tree1.xsecWeight):
                                continue
			#Testing if it is a true event
			for p in range (tree1.nTrueSimParts):
				if tree1.trueSimPartProcess[p] !=0:
					continue

				detCrds = [[0., 256.35], [-116.5, 116.5], [0, 1036.8]]
				def inRange(x, bound):
					return (x >= bound[0] and x <= bound[1])
				def isInDetector(X,Y,Z):
					return (inRange(X, detCrds[0]), inRange(Y,detCrds[1]), inRange(Z,detCrds[2]))

				if tree1.trueSimPartPDG[p] == 22:
					PhotonInDetector = False
					if isInDetector(tree1.trueSimPartEDepX[p],tree1.trueSimPartEDepY[p], tree1.trueSimPartEDepZ[p]) == (True, True, True):
						PhotonInDetector = True
					if PhotonInDetector == True:
						showerCount += 1
				if tree1.trueSimPartPDG[p] == 11 or tree1.trueSimPartPDG[p] == -11:
					ElectronInDetector = False
					if isInDetector(tree1.trueSimPartEDepX[p],tree1.trueSimPartEDepY[p], tree1.trueSimPartEDepZ[p]) == (True, True, True):
						ElectronInDetector = True
					if ElectronInDetector == True:
						showerCount += 1
				if tree1.trueSimPartPDG[p] == 13 or tree1.trueSimPartPDG[p] == -13:
					if tree1.trueSimPartE[p] > 144.3:
						muonCount += 1
				if tree1.trueSimPartPDG[p] == 211 or tree1.trueSimPartPDG[p] == -211:
					if tree1.trueSimPartE[p] > 190.6:
						pionCount += 1
				if tree1.trueSimPartPDG[p] == 2212 or tree1.trueSimPartPDG[p] == -2212:
					if tree1.trueSimPartE[p] > 1288.3:
						protonCount += 1
			
			for p in range (tree1.nTruePrimParts):
				if tree1.truePrimPartPDG[p] == 111:
					NpionCount += 1
			if showerCount != 1:
				TrueEvent = "False"
			if muonCount != 0 or protonCount != 0 or pionCount != 0 or NpionCount != 0:
				TrueEvent = "False"


			#testing if it is a reco event
			primCompShowers = 0
			for s in range(tree1.nShowers):
				if tree1.showerClassified[s] == 1 and tree1.showerComp[s] > 0.4: 
					if tree1.showerPID[s] != 22 and tree1.showerPID[s] != 11 and tree1.showerPID[s] != -11:
						RecoEvent = "False"
						continue
					ElPhmPiScore = 0 
					if tree1.showerElScore[s] >= tree1.showerPhScore[s]:
						ElPhmPiScore = tree1.showerElScore[s] - tree1.showerPiScore[s]
					if tree1.showerPhScore[s] > tree1.showerElScore[s]:
						ElPhmPiScore = tree1.showerPhScore[s] - tree1.showerPiScore[s]
					if ElPhmPiScore < 10.3:
						RecoEvent = "False"
						continue
					primCompShowers += 1
			if primCompShowers != 1:
				RecoEvent = "False"

			if tree1.foundVertex != 1:
				RecoEvent = "False"
			if tree1.vtxIsFiducial != 1:
				RecoEvent = "False"
			if tree1.vtxFracHitsOnCosmic >= 1:
				RecoEvent = "False"
			for t in range(tree1.nTracks):
				if tree1.trackIsSecondary[t] == 1 or tree1.trackClassified[t] !=1:
					continue
				if tree1.trackPID[t] == 211: #pions
					if tree1.trackRecoE[t] >= 51.0:
						RecoEvent = "False"
				if tree1.trackPID[t] == 13: #muons
					if tree1.trackRecoE[t] >= 38.6:
						RecoEvent = "False"
				if tree1.trackPID[t] == 2212: #protons
					if tree1.trackRecoE[t] >= 350:
						RecoEvent = "False"
			if TrueEvent == "True":
				CCeTrue.Fill(tree1.trueNuE, tree1.xsecWeight)
				TrueEvents += tree1.xsecWeight*scale1

			if TrueEvent == "True" and RecoEvent == "True":
				CCeTrueReco.Fill(tree1.trueNuE, tree1.xsecWeight)
				recoTruePurityCCe.Fill(tree1.recoNuE, tree1.xsecWeight)
				TrueAndRecoEvents += tree1.xsecWeight*scale1
			if RecoEvent == "True":
				recoPurityCCe.Fill(tree1.recoNuE, tree1.xsecWeight)
				RecoEvents +=tree1.xsecWeight*scale1

			#if RecoEvent == "True" and TrueEvent != "True":



#Filling From Tree 3
for i in range (tree3.GetEntries()):
			tree3.GetEntry(i)
			tracksFit = True
				
			primCompShowers = 0
			for s in range(tree3.nShowers):
				#if tree3.showerIsSecondary[s] != 1 and tree3.showerClassified[s] == 1 and tree3.showerComp[s] > 0.45:
				#	if tree3.showerPID[s] != 22 and tree3.showerPID[s] != 11 and tree3.showerPID[s] != -11:
				#		continue
				if tree3.showerClassified[s] == 1 and tree3.showerComp[s] > 0.4:
					if tree3.showerPID[s] != 22 and tree3.showerPID[s] != 11 and tree3.showerPID[s] != -11:
						continue

					ElPhmPiScore = 0 
					if tree3.showerElScore[s] >= tree3.showerPhScore[s]:
						ElPhmPiScore = tree3.showerElScore[s] - tree3.showerPiScore[s]
					if tree3.showerPhScore[s] > tree3.showerElScore[s]:
						ElPhmPiScore = tree3.showerPhScore[s] - tree3.showerPiScore[s]

					if ElPhmPiScore < 10.3:
						RecoEvent = "False"
						continue

					primCompShowers += 1

			if primCompShowers != 1:
				continue
			
			if tree3.nVertices < 1:
				continue
			if tree3.vtxIsFiducial != 1:
				continue
			if tree3.vtxFracHitsOnCosmic >= 1:
				continue
			for t in range(tree3.nTracks):
				if tree3.trackIsSecondary[t] == 1 or tree3.trackClassified[t] !=1:
					continue
				if tree3.trackPID[t] == 211: #pions
					if tree3.trackRecoE[t] >= 51.0:
						tracksFit = False
						continue
				if tree3.trackPID[t] == 13: #muons
					if tree3.trackRecoE[t] >= 38.6:
						tracksFit = False
						continue
				if tree3.trackPID[t] == 2212: #protons
					if tree3.trackRecoE[t] >= 350:
						tracksFit = False
						continue
			if tracksFit == False: 
					continue
			recoPurityCB.Fill(tree3.recoNuE)
			RecoEvents += tree3.xsecWeight*scale3
			

#Printing Variables
print(f"True and Reco Events: {TrueAndRecoEvents}")
print(f"Reco Events: {RecoEvents}")
print(f"True Events: {TrueEvents}")

Purity = TrueAndRecoEvents/RecoEvents
Efficiency = TrueAndRecoEvents/TrueEvents

print(f"Purity: {Purity}")
print(f"Efficiency: {Efficiency}")


#Scaling Histograms

CCeTrue.Sumw2(1)
NCeTrue.Sumw2(1)
NCmTrue.Sumw2(1)
CCmTrue.Sumw2(1)
                
CCeTrueReco.Sumw2(1)
NCeTrueReco.Sumw2(1)
NCmTrueReco.Sumw2(1)
CCmTrueReco.Sumw2(1)

CCeTrue.Scale(dataPot1/totPot1)
NCeTrue.Scale(dataPot2/totPot2)
NCmTrue.Scale(dataPot2/totPot2)
CCmTrue.Scale(dataPot2/totPot2)


CCeTrueReco.Scale(dataPot1/totPot1)        
NCeTrueReco.Scale(dataPot2/totPot2)                 
NCmTrueReco.Scale(dataPot2/totPot2) 
CCmTrueReco.Scale(dataPot2/totPot2) 


#Printing histograms:

canvas = rt.TCanvas("canvas")
canvas.cd()

def printHistoSame(histoName, XaxisName, LineWidth, LineColor):
                histoName.Draw("HIST, same")
                histoName.GetYaxis().SetTitle("Events Per 6.67e20 pot")
                histoName.GetXaxis().SetTitle(XaxisName)
                histoName.SetLineWidth(LineWidth)
                histoName.SetLineColor(LineColor)
                canvas.Print()
               	input("Press Enter to continue...")

	
printHistoSame(CCeTrue, "True Neutrino Energy", 2, rt.kBlue)
printHistoSame(CCmTrue, "True Neutrino Energy", 2, rt.kViolet)
printHistoSame(NCeTrue, "", 2, rt.kGreen)
printHistoSame(NCmTrue, "", 2, rt.kRed)
	
canvas.SetLogy()
legend = rt.TLegend (0.7, 0.6, 0.85, 0.75)
legend.AddEntry(CCeTrue, "CC eNu")
legend.AddEntry(NCeTrue, "NC eNu")
legend.AddEntry(CCmTrue, "CC mNu")
legend.AddEntry(NCmTrue, "NC mNu")
legend.Draw("same")
#canvas.Print()
input("press")


recoCanvas = rt.TCanvas("rCanvas")
recoCanvas.cd()

def printHistoSameReco(histoName, XaxisName, LineWidth, LineColor):
                histoName.Draw("HIST, same")
                histoName.GetYaxis().SetTitle("Events Per 6.67e20 pot")
                histoName.GetXaxis().SetTitle(XaxisName)
                histoName.SetLineWidth(LineWidth)
                histoName.SetLineColor(LineColor)
                recoCanvas.Print()
                input("Press Enter to continue...")

printHistoSameReco(CCeTrueReco, "True Neutrino Energy", 2, rt.kBlue)
printHistoSameReco(CCmTrueReco, "True Neutrino Energy", 2, rt.kViolet)
printHistoSameReco(NCeTrueReco, "", 2, rt.kGreen)
printHistoSameReco(NCmTrueReco, "", 2, rt.kRed)  

recoCanvas.SetLogy()
rlegend = rt.TLegend (0.7, 0.6, 0.85, 0.75)      
rlegend.AddEntry(CCeTrue, "CC eNu")
rlegend.AddEntry(NCeTrue, "NC eNu")
rlegend.AddEntry(CCmTrue, "CC mNu")
rlegend.AddEntry(NCmTrue, "NC mNu")     
rlegend.Draw("same")
recoCanvas.Print()
input("press")


AllTrueMBHisto = rt.TH1F("TrueMB", "TrueNuE for All True MiniBooNE Events", 100,0,5)
AllTrueMBHisto.Add(CCeTrue)
AllTrueMBHisto.Add(CCmTrue)
AllTrueMBHisto.Add(NCmTrue)
AllTrueMBHisto.Add(NCeTrue)

AllTrueMBHistoCanvas = rt.TCanvas("AllTrueMBHistoCanvas")
AllTrueMBHistoCanvas.cd()
AllTrueMBHisto.Draw("HIST")
AllTrueMBHistoCanvas.Print()
input("press")


AllTrueAndRecoMBHisto = rt.TH1F("TrueAndRecoMB", "TrueNuE for All True and Reconstructed  MiniBooNE Events", 100,0,5)
AllTrueAndRecoMBHisto.Add(CCeTrueReco)
AllTrueAndRecoMBHisto.Add(CCmTrueReco)
AllTrueAndRecoMBHisto.Add(NCeTrueReco)
AllTrueAndRecoMBHisto.Add(NCeTrueReco)

AllTrueAndRecoMBHistoCanvas = rt.TCanvas("AllTrueAndRecoMBHistoCanvas")
AllTrueAndRecoMBHistoCanvas.cd()
AllTrueAndRecoMBHisto.Draw("HIST")
AllTrueAndRecoMBHistoCanvas.Print()
input("press")


AllTrueAndRecoMBHisto.Divide(AllTrueMBHisto)
efficiencyHisto = rt.TH1F("efficiency", "Efficiency", 100,0,5)
efficiencyHisto.Add(AllTrueAndRecoMBHisto)
efficiencyHisto.Sumw2()


eCanvas = rt.TCanvas("eCanvas")
eCanvas.cd()
efficiencyHisto.Draw("E")
efficiencyHisto.GetXaxis().SetTitle("True NuE")
efficiencyHisto.SetLineWidth(2)
efficiencyHisto.SetLineColor(rt.kViolet)
eCanvas.Print()
input("Press Enter to continue...")


recoPurityCB.Scale(dataPot3/totPot3) #have to see what to do with cb events
recoPurityCCe.Scale(dataPot1/totPot1)
recoPurityNCe.Scale(dataPot2/totPot2)
recoPurityNCm.Scale(dataPot2/totPot2)
recoPurityCCm.Scale(dataPot2/totPot2)

recoTruePurityNCm.Scale(dataPot2/totPot2)
recoTruePurityNCe.Scale(dataPot2/totPot2)
recoTruePurityCCm.Scale(dataPot2/totPot2)
recoTruePurityCCe.Scale(dataPot1/totPot1)

RecoPurityC = rt.TCanvas("reco")
RecoPurityC.cd()

def printHistoRecoPurity(histoName, XaxisName, LineWidth, LineColor):
                histoName.Draw("HIST, same")
                histoName.GetYaxis().SetTitle("Events Per 6.67e20 pot")
                histoName.GetXaxis().SetTitle(XaxisName)
                histoName.SetLineWidth(LineWidth)
                histoName.SetLineColor(LineColor)
                RecoPurityC.Print()
                input("Press Enter to continue...")

RecoPurityC.SetLogy()
printHistoRecoPurity(recoPurityCB, "Reco NuE", 2, rt.kOrange)
printHistoRecoPurity(recoPurityNCm, "Reco NuE", 2, rt.kRed)
printHistoRecoPurity(recoPurityNCe, "Reco NuE", 2, rt.kGreen)
printHistoRecoPurity(recoPurityCCm, "Reco NuE", 2, rt.kViolet)
printHistoRecoPurity(recoPurityCCe, "Reco NuE", 2, rt.kBlue)
RecoPurityC.SetLogy()
input("press")


RecoTruePurityC = rt.TCanvas("recoTrue")
RecoTruePurityC.cd()

def printHistoRecoTruePurity(histoName, XaxisName, LineWidth, LineColor):
                histoName.Draw("HIST, same")
                histoName.GetYaxis().SetTitle("Events Per 6.67e20 pot")
                histoName.GetXaxis().SetTitle(XaxisName)
                histoName.SetLineWidth(LineWidth)
                histoName.SetLineColor(LineColor)
                RecoTruePurityC.Print()
                input("Press Enter to continue...")

RecoTruePurityC.SetLogy()
printHistoRecoTruePurity(recoTruePurityNCm, "Reco NuE", 2, rt.kRed)
printHistoRecoTruePurity(recoTruePurityNCe, "Reco NuE", 2, rt.kGreen)
printHistoRecoTruePurity(recoTruePurityCCm, "Reco NuE", 2, rt.kViolet)
printHistoRecoTruePurity(recoTruePurityCCe, "Reco NuE", 2, rt.kBlue)
RecoTruePurityC.Print()
input("press")


AllRecoPurity = rt.TH1F("AllReco", "Reco NuE for Reco MiniBoone Events", 30, 0, 3000)
AllRecoTruePurity = rt.TH1F("AllRecoTrue", "Reco NuE for Reco and True MiniBooNE Events", 30, 0, 3000)
AllRecoPurity.Add(recoPurityCB) 
AllRecoPurity.Add(recoPurityCCe)
AllRecoPurity.Add(recoPurityCCm)
AllRecoPurity.Add(recoPurityNCm)
AllRecoPurity.Add(recoPurityNCe)


AllRecoPurityCanvas = rt.TCanvas("AllRecoPurityCanvas")
AllRecoPurityCanvas.cd()
AllRecoPurity.Draw("HIST")
AllRecoPurity.SetAxisRange(0.1, 10000,"Y")
AllRecoPurityCanvas.Print()
input("press")


AllRecoTruePurity.Add(recoTruePurityCCm)
AllRecoTruePurity.Add(recoTruePurityCCe)
AllRecoTruePurity.Add(recoTruePurityNCm)
AllRecoTruePurity.Add(recoTruePurityNCe)


AllRecoTruePurityCanvas = rt.TCanvas("AllRecoTruePurityCanvas")
AllRecoTruePurityCanvas.cd()
AllRecoTruePurity.Draw("HIST")
AllRecoTruePurity.SetAxisRange(0.1, 200,"Y")
AllRecoTruePurityCanvas.Print()
input("press")


PurityHisto = rt.TH1F("purity", "Purity", 30, 0, 3000)
AllRecoTruePurity.Divide(AllRecoPurity)
PurityHisto.Add(AllRecoTruePurity)	
purityCanvas = rt.TCanvas("purity")
purityCanvas.cd()
PurityHisto.Draw("E")
PurityHisto.GetXaxis().SetTitle("Reco NuE")
PurityHisto.SetLineWidth(2)
purityCanvas.Print()
input("press")
