import os
import ROOT
from ROOT import *
from array import array
import math
from math import *
import sys
import Plotting_Header
from Plotting_Header import *

def ComputeDDT(name, point, nPtBins, nRhoBins, H):
	DDT = TH2F(name, "", nRhoBins, -8.5, -1.5, nPtBins, 175, 775)
	DDT.SetStats(0)
	nXb = H.GetXaxis().GetNbins()
	nYb = H.GetYaxis().GetNbins()
	for x in range(nXb):
		for y in range(nYb):
			proj = H.ProjectionZ("H3"+str(x)+str(y),x+1,x+1,y+1,y+1)
			print str(x+1) + "," + str(y+1) + ":    "+ str(proj.Integral())
			p = array('d', [point])
			q = array('d', [0.0]*len(p))
			proj.GetQuantiles(len(p), q, p)
			DDT.SetBinContent( x+1, y+1, q[0] );
	return DDT

def DisplayDDT(DDT):
	C = TCanvas("TempCanvas", "Title", 820, 640)
	C.cd()
	DDT.SetStats(0)
	DDT.GetXaxis().SetTitle("jet #rho")
	DDT.GetYaxis().SetTitle("jet p_{T}")
	DDT.GetYaxis().SetTitleOffset(1.35)
	DDT.Draw("COLZ")
	C.Print("DDT_Map.png")

def FillEst(DDT, Bkgs):

	NonResPass = TH1F("NRP", "", 40, 5, 255)
	NonResFail = TH1F("NRF", "", 40, 5, 255)
	Sig25 = TH1F("S25", "", 40, 5, 255)
	Sig25short = TH1F("S25s", "", 40, 5, 255)
	F = TFile("/uscms_data/d3/rapte/bits/VectorDiJet1Gamma_M25.root")
	T = F.Get("Events")
	n = T.GetEntries()
	for j in range(0, n): # Here is where we loop over all events.
		T.GetEntry(j)
		weight = T.puWeight*T.scale1fb*T.kfactor*T.kfactorNLO
		PT = T.AK8Puppijet0_pt
		M = T.AK8Puppijet0_msd
		if (T.AK8Puppijet0_N2sdb1 > 0. and M*M/PT/PT) > 0.0 and PT > 175 and PT < 775 and M>6:
			RHO = math.log(M*M/PT/PT)
			rind = DDT.GetXaxis().FindBin(RHO)
			pind = DDT.GetYaxis().FindBin(PT)


			if RHO >  DDT.GetXaxis().GetBinUpEdge( DDT.GetXaxis().GetNbins() ) :
				rind = DDT.GetXaxis().GetNbins()
			if RHO <  DDT.GetXaxis().GetBinLowEdge( 1 ) :
				rind = 1 
			if PT >  DDT.GetYaxis().GetBinUpEdge( DDT.GetYaxis().GetNbins() ) :
				pind = DDT.GetYaxis().GetNbins()
			if PT < DDT.GetYaxis().GetBinLowEdge( 1 ) :
				pind = 1

			N2DDT = T.AK8Puppijet0_N2sdb1 - DDT.GetBinContent(rind,pind)
			if RHO > -8.5:
				if N2DDT < 0: #pass
					Sig25.Fill(M,weight)
					if RHO > -6.0:
						Sig25short.Fill(M,weight)
	for B in Bkgs:
		F = TFile(B)
		T = F.Get("Events")
		n = T.GetEntries()
		for j in range(0, n): # Here is where we loop over all events.
			T.GetEntry(j)
			weight = T.puWeight*T.scale1fb*T.kfactor*T.kfactorNLO
			PT = T.AK8Puppijet0_pt
			M = T.AK8Puppijet0_msd
			if (T.AK8Puppijet0_N2sdb1 > 0. and M*M/PT/PT) > 0.0 and PT > 175 and PT < 775 and M>6:
				RHO = math.log(M*M/PT/PT)
				rind = DDT.GetXaxis().FindBin(RHO)
				pind = DDT.GetYaxis().FindBin(PT)


				if RHO >  DDT.GetXaxis().GetBinUpEdge( DDT.GetXaxis().GetNbins() ) :
					rind = DDT.GetXaxis().GetNbins()
				if RHO <  DDT.GetXaxis().GetBinLowEdge( 1 ) :
					rind = 1 
				if PT >  DDT.GetYaxis().GetBinUpEdge( DDT.GetYaxis().GetNbins() ) :
					pind = DDT.GetYaxis().GetNbins()
				if PT < DDT.GetYaxis().GetBinLowEdge( 1 ) :
					pind = 1

				N2DDT = T.AK8Puppijet0_N2sdb1 - DDT.GetBinContent(rind,pind)
				if  RHO < -1.5 and RHO > -8.5:
					if N2DDT < 0: #pass
						NonResPass.Fill(M,weight)
					else: #fail
						NonResFail.Fill(M,weight)

	NonResFail.Scale(5./95.)

	FindAndSetMax([NonResPass, NonResFail])

	leg = TLegend(0.475,0.385,0.85,0.89)
	leg.SetHeader("QCD & #gamma + jets MCs (DDT~5%):")
	leg.AddEntry(NonResPass, "events N_{2}^{DDT} < 0", "PL")
	leg.AddEntry(NonResFail, "#frac{5}{95} #times events N_{2}^{DDT} > 0", "L")
	leg.SetLineColor(0)
	leg.SetFillColor(0)

	Sig25.SetLineColor(kRed)
	Sig25.SetFillColor(kRed-2)
	Sig25.SetFillStyle(3004)
	Sig25short.SetLineColor(kRed)
	Sig25short.SetFillColor(kRed-2)
	Sig25short.SetFillStyle(3005)
	Sig25short.Scale(0.2)
	Sig25.Scale(0.2)

	NonResPass.Sumw2()
	NonResPass.SetLineColor(1)
	NonResPass.SetFillColor(0)
	NonResPass.SetMarkerColor(1)
	NonResPass.SetMarkerStyle(20)

	NonResFail.SetStats(0)
	NonResFail.SetLineColor(kGreen)
	NonResFail.SetLineWidth(2)
	NonResFail.GetXaxis().SetTitle("AK8 Soft Drop Mass [GeV]")
	NonResFail.GetYaxis().SetTitle("Events")
	NonResFail.GetXaxis().SetTitleSize(0.045)
	NonResFail.GetYaxis().SetTitleSize(0.045)


	C = TCanvas("C", "", 800, 600)
	C.cd()
	CMSLABL = TLatex()
	CMSLABL.SetNDC()
	CMSLABL.SetTextSize(0.045)
	PRELABL = TLatex()
	PRELABL.SetNDC()
	PRELABL.SetTextSize(0.04)
	THILABL = TLatex()
	THILABL.SetNDC()
	THILABL.SetTextSize(0.045)
	NonResFail.Draw("hist")
	NonResPass.Draw("E0 same")
	leg.Draw("same")
	C.Print("DDT_SanityCheck.png")


RB = 28
PB = 24
H3 = TH3F("H3", "", RB, -8.5, -1.5, PB, 175, 775, 500, 0, 0.5)
H3.SetStats(0)
Bkgs =["GJetsmvaEVv3.root", "QCDmvaEVwithExtv3.root"]
for B in Bkgs:
	F = TFile(B)
	T = F.Get("Events")
	n = T.GetEntries()
	for j in range(0, n): # Here is where we loop over all events.
		T.GetEntry(j)
		if tree.neleLoose == 0 and tree.nmuLoose == 0 and tree.ntau==0 and tree.nphoLoose==0 and tree.AK8Puppijet0_isTightVJet ==1:
			weight = T.puWeight*T.scale1fb*T.kfactor*T.kfactorNLO
			PT = T.AK8Puppijet0_pt
			if PT > 175.:
			    preRHO = T.AK8Puppijet0_msd*T.AK8Puppijet0_msd/T.AK8Puppijet0_pt/T.AK8Puppijet0_pt
			    if preRHO > 0.:
				RHO = math.log(preRHO)
				if RHO < -1.5 and RHO > -8.5 and T.AK8Puppijet0_N2sdb1 > 0. and T.AK8Puppijet0_msd > 6.:
					H3.Fill(RHO, PT, T.AK8Puppijet0_N2sdb1, weight)

DDT = ComputeDDT("DDT", 0.05, PB, RB, H3)
DisplayDDT(DDT)

# Check Estimate:
FillEst(DDT, Bkgs)

Fout = TFile("PhotonDDTs.root", "recreate")
Fout.cd()
DDT.Write()
Fout.Close()
