FIN_THETA="../correlator_data/matching_windows_theta_q99.root"
FIN_PHI="../correlator_data/matching_windows_phi_q99.root"

FOUT_THETA="../correlator_data/quantized/matching_windows_theta_q99_wrlx_x2to6_y0to0p5.root"
FOUT_PHI="../correlator_data/quantized/matching_windows_phi_q99_wrlx_x2to6_y0to0p5.root"

root -l -b -q embed_relaxation.C'("'${FIN_THETA}'", "'${FOUT_THETA}'")' 
root -l -b -q embed_relaxation.C'("'${FIN_PHI}'", "'${FOUT_PHI}'")'
