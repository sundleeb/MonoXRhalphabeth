import os
import math
from array import array
import optparse
import ROOT
from ROOT import *
import sys

def createHist(tag,filename):
	infolder = '/uscms_data/d3/matteoc/panda/v_8026_0_4/flat//rhalphabeth//signal/'

	massbins = 100;
	masslo   = 30;
	masshi   = 1000;

	ptbins = 4;
	ptlo = 200;
	pthi = 1600;

	h_pass_ca15 = TH2F(tag+"_pass","; CA15 m_{SD}^{PUPPI} (GeV); CA15 p_{T} (GeV)",massbins,masslo,masshi,ptbins,ptlo,pthi)
	h_fail_ca15 = TH2F(tag+"_fail","; CA15 m_{SD}^{PUPPI} (GeV); CA15 p_{T} (GeV)",massbins,masslo,masshi,ptbins,ptlo,pthi)
	h_pass_matched_ca15 = TH2F(tag+"_pass_matched","; CA15 m_{SD}^{PUPPI} (GeV); CA15 p_{T} (GeV)",massbins,masslo,masshi,ptbins,ptlo,pthi)
	h_pass_unmatched_ca15 = TH2F(tag+"_pass_unmatched","; CA15 m_{SD}^{PUPPI} (GeV); CA15 p_{T} (GeV)",massbins,masslo,masshi,ptbins,ptlo,pthi)
	h_fail_matched_ca15 = TH2F(tag+"_fail_matched","; CA15 m_{SD}^{PUPPI} (GeV); CA15 p_{T} (GeV)",massbins,masslo,masshi,ptbins,ptlo,pthi)
	h_fail_unmatched_ca15 = TH2F(tag+"_fail_unmatched","; CA15 m_{SD}^{PUPPI} (GeV); CA15 p_{T} (GeV)",massbins,masslo,masshi,ptbins,ptlo,pthi)
	
	# validation
	h_pass_msd_ca15 = TH1F(tag+"pass_msd", "; CA15 m_{SD}^{PUPPI}; N", 60, 0, 300)
	h_fail_msd_ca15 = TH1F(tag+"fail_msd", "; CA15 m_{SD}^{PUPPI}; N", 60, 0, 300)
	h_pass_msd_matched_ca15 = TH1F(tag+"pass_msd_matched", "; CA15 m_{SD}^{PUPPI}; N", 60, 0, 300)
	h_pass_msd_unmatched_ca15 = TH1F(tag+"pass_msd_unmatched", "; CA15 m_{SD}^{PUPPI}; N", 60, 0, 300)
	h_fail_msd_matched_ca15 = TH1F(tag+"fail_msd_matched", "; CA15 m_{SD}^{PUPPI}; N", 60, 0, 300)
	h_fail_msd_unmatched_ca15 = TH1F(tag+"fail_msd_unmatched", "; CA15 m_{SD}^{PUPPI}; N", 60, 0, 300)

	print filename+".root"
	infile=ROOT.TFile(infolder+filename+".root")	

	tree= infile.Get("Events")
	nent = tree.GetEntries();

	for i in range(tree.GetEntries()):

		tree.GetEntry(i)
		if(i % (1 * nent/100) == 0):
			sys.stdout.write("\r[" + "="*int(20*i/nent) + " " + str(round(100.*i/nent,0)) + "% done")
			sys.stdout.flush()

		#puweight = tree.puWeight
		#fbweight = tree.scale1fb * lumi
		weight = tree.weight
		#if isdata: weight = puweight*fbweight

		jmsd_8 = tree.fjmass
		PT = tree.fjpt
		DDT = tree.n2ddt56

		# non resonant case
		#jphi  = 9999;
		#dphi  = 9999;
		#dpt   = 9999;
		#dmass = 9999;
		#if mass > 0:
		#	jphi = getattr(tree,"AK8Puppijet0_phi");
		#	dphi = math.fabs(tree.genVPhi - jphi)
		#       dpt = math.fabs(tree.genVPt - PT)/tree.genVPt
		#	dmass = math.fabs(mass - jmsd_8)/mass
		
		
		# pass category		
		if PT > 200. and PT < 1600.:
				if DDT < 0:
					h_pass_ca15.Fill( jmsd_8, PT, weight )
					## for signal morphing
					h_pass_msd_ca15.Fill( jmsd_8, weight );
					#if dphi < 0.8 and dpt < 0.5 and dmass < 0.3:
					#	h_pass_msd_matched_ca15.Fill( jmsd_8, weight );
					#	h_pass_matched_ca15.Fill( jmsd_8, PT, weight );
					#else:
					#	h_pass_msd_unmatched_ca15.Fill( jmsd_8, weight );
					#	h_pass_unmatched_ca15.Fill( jmsd_8, PT, weight );
				# fail category
				if DDT > 0:
					h_fail_ca15.Fill( jmsd_8, PT, weight )
					## for signal morphing
					h_fail_msd_ca15.Fill( jmsd_8, weight );
					#if dphi < 0.8 and dpt < 0.5 and dmass < 0.3:
					#	h_fail_msd_matched_ca15.Fill( jmsd_8, weight );
					#	h_fail_matched_ca15.Fill( jmsd_8, PT, weight );
					#else:
					#	h_fail_msd_unmatched_ca15.Fill( jmsd_8, weight );	
					#	h_fail_unmatched_ca15.Fill( jmsd_8, PT, weight );

	hists_out = [];
	#2d histograms
	hists_out.append( h_pass_ca15 );
	hists_out.append( h_fail_ca15 );
	#hists_out.append( h_pass_matched_ca15 );
	#hists_out.append( h_pass_unmatched_ca15 );
	#hists_out.append( h_fail_matched_ca15 );
	#hists_out.append( h_fail_unmatched_ca15 );
	#1d validation histograms
	hists_out.append( h_pass_msd_ca15 );
	#hists_out.append( h_pass_msd_matched_ca15 );
	#hists_out.append( h_pass_msd_unmatched_ca15 );
	hists_out.append( h_fail_msd_ca15 );
	#hists_out.append( h_fail_msd_matched_ca15 );
	#hists_out.append( h_fail_msd_unmatched_ca15 );

	return hists_out

outfile=TFile("MonoXTemplates.root", "recreate");
lumi =36.600
#lumi = 2.44
#SF_tau21 =1

data_hists = createHist('data','fittingForest_MET')
diboson_hists = createHist('diboson','fittingForest_Diboson')
#qcd_hists = createHist('qcd','fittingForest_QCD')      
stop_hists = createHist('stop','fittingForest_SingleTop')
ttbar_hists = createHist('ttbar','fittingForest_TTbar')    
wjets_hists = createHist('wjets','fittingForest_WJets')    
zjets_hists = createHist('zjets','fittingForest_ZJets')    

mass=[600,800,1000,1200,1400,1700,2000,2500]

for m in mass:
	hs_hists = createHist('ZpA0h%s'%(m),'fittingForest_ZpA0h_med-%s_dm-300'%(m))
	outfile.cd()
	for h in hs_hists: h.Write();

print("Building pass/fail")	
outfile.cd()
for h in data_hists: h.Write();
for h in diboson_hists: h.Write();
#for h in qcd_hists: h.Write();
for h in stop_hists: h.Write();
for h in ttbar_hists: h.Write();
for h in wjets_hists: h.Write();
for h in zjets_hists: h.Write();
outfile.Write()
outfile.Close()

