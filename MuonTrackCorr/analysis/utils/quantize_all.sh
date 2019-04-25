#### make the quantization of all functions
#### the phi max is at 2, eta max is at 0.5
#### considering phi only (max range), I need
#### 11 bit -> 0.001 precision
#### 10 bit -> 0.002 precision
#### 9 bit  -> 0.004 precision

for X_PREC in 0.5 1.0; do
    for Y_PREC in 0.001 0.002 0.004; do
        
        echo "... doing ${X_PREC}, ${Y_PREC}"

        # X_PREC="0.5"
        # Y_PREC="0.005"

        # FIN_THETA="../correlator_data/matching_windows_theta_q99.root"
        # FIN_PHI="../correlator_data/matching_windows_phi_q99.root"

        # FOUT_THETA="../correlator_data/quantized/matching_windows_theta_q99_x${X_PREC}_y${Y_PREC}.root"
        # FOUT_PHI="../correlator_data/quantized/matching_windows_phi_q99_x${X_PREC}_y${Y_PREC}.root"

        FIN_THETA="../correlator_data/quantized/matching_windows_theta_q99_wrlx_x2to6_y0to0p5.root"
        FIN_PHI="../correlator_data/quantized/matching_windows_phi_q99_wrlx_x2to6_y0to0p5.root"

        FOUT_THETA="../correlator_data/quantized/matching_windows_theta_q99_wrlx_x2to6_y0to0p5__x${X_PREC}_y${Y_PREC}.root"
        FOUT_PHI="../correlator_data/quantized/matching_windows_phi_q99_wrlx_x2to6_y0to0p5__x${X_PREC}_y${Y_PREC}.root"


        root -l -b -q quantize_windows_TF1.C'("'${FIN_THETA}'", "'${FOUT_THETA}'", '${X_PREC}', '${Y_PREC}')'
        root -l -b -q quantize_windows_TF1.C'("'${FIN_PHI}'", "'${FOUT_PHI}'", '${X_PREC}', '${Y_PREC}')'
    done
done