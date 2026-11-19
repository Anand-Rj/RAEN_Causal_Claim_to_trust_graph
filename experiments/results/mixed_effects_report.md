# Mixed-effects, McNemar and robustness (test split)
banners: ['LLM:anthropic/claude-haiku-5.5 | profiles:measured', 'LLM:meta-llama/llama-3.3-70b-instruct | profiles:measured', 'LLM:openai/gpt-4o-mini | profiles:measured']

## Mixed model: tce   (crossed variance components: task + model family)

```
                                          Mixed Linear Model Regression Results
==========================================================================================================================
Model:                                   MixedLM                       Dependent Variable:                       tce      
No. Observations:                        3360                          Method:                                   REML     
No. Groups:                              1                             Scale:                                    0.0005   
Min. group size:                         3360                          Log-Likelihood:                           7839.2201
Max. group size:                         3360                          Converged:                                Yes      
Mean group size:                         3360.0                                                                           
--------------------------------------------------------------------------------------------------------------------------
                                                                               Coef.  Std.Err.    z    P>|z| [0.025 0.975]
--------------------------------------------------------------------------------------------------------------------------
Intercept                                                                       0.037    0.005   7.858 0.000  0.028  0.046
C(cond, Treatment('outcome'))[T.graph]                                         -0.010    0.003  -3.560 0.000 -0.016 -0.005
C(cond, Treatment('outcome'))[T.graph_masked]                                  -0.003    0.003  -1.105 0.269 -0.009  0.002
C(cond, Treatment('outcome'))[T.graph_rule]                                    -0.037    0.003 -12.831 0.000 -0.042 -0.031
C(cond, Treatment('outcome'))[T.raw]                                            0.006    0.003   1.917 0.055 -0.000  0.011
C(cond, Treatment('outcome'))[T.raw_cot]                                        0.004    0.003   1.293 0.196 -0.002  0.009
C(cond, Treatment('outcome'))[T.skill]                                         -0.009    0.003  -3.177 0.001 -0.015 -0.003
C(cause)[T.out_of_specialty]                                                    0.031    0.003  10.898 0.000  0.026  0.037
C(cause)[T.persistent_reasoning]                                                0.091    0.003  31.513 0.000  0.085  0.096
C(cause)[T.tool_failure]                                                        0.000    0.003   0.024 0.981 -0.006  0.006
C(cond, Treatment('outcome'))[T.graph]:C(cause)[T.out_of_specialty]            -0.034    0.004  -8.476 0.000 -0.042 -0.026
C(cond, Treatment('outcome'))[T.graph_masked]:C(cause)[T.out_of_specialty]     -0.038    0.004  -9.436 0.000 -0.046 -0.030
C(cond, Treatment('outcome'))[T.graph_rule]:C(cause)[T.out_of_specialty]       -0.019    0.004  -4.629 0.000 -0.027 -0.011
C(cond, Treatment('outcome'))[T.raw]:C(cause)[T.out_of_specialty]              -0.009    0.004  -2.116 0.034 -0.017 -0.001
C(cond, Treatment('outcome'))[T.raw_cot]:C(cause)[T.out_of_specialty]          -0.006    0.004  -1.417 0.156 -0.014  0.002
C(cond, Treatment('outcome'))[T.skill]:C(cause)[T.out_of_specialty]            -0.047    0.004 -11.689 0.000 -0.055 -0.040
C(cond, Treatment('outcome'))[T.graph]:C(cause)[T.persistent_reasoning]         0.013    0.004   3.311 0.001  0.005  0.021
C(cond, Treatment('outcome'))[T.graph_masked]:C(cause)[T.persistent_reasoning] -0.010    0.004  -2.429 0.015 -0.018 -0.002
C(cond, Treatment('outcome'))[T.graph_rule]:C(cause)[T.persistent_reasoning]   -0.008    0.004  -2.090 0.037 -0.016 -0.001
C(cond, Treatment('outcome'))[T.raw]:C(cause)[T.persistent_reasoning]          -0.015    0.004  -3.792 0.000 -0.023 -0.007
C(cond, Treatment('outcome'))[T.raw_cot]:C(cause)[T.persistent_reasoning]      -0.013    0.004  -3.091 0.002 -0.021 -0.005
C(cond, Treatment('outcome'))[T.skill]:C(cause)[T.persistent_reasoning]         0.008    0.004   2.003 0.045  0.000  0.016
C(cond, Treatment('outcome'))[T.graph]:C(cause)[T.tool_failure]                 0.012    0.004   3.040 0.002  0.004  0.020
C(cond, Treatment('outcome'))[T.graph_masked]:C(cause)[T.tool_failure]          0.008    0.004   2.009 0.045  0.000  0.016
C(cond, Treatment('outcome'))[T.graph_rule]:C(cause)[T.tool_failure]           -0.000    0.004  -0.017 0.986 -0.008  0.008
C(cond, Treatment('outcome'))[T.raw]:C(cause)[T.tool_failure]                   0.014    0.004   3.448 0.001  0.006  0.022
C(cond, Treatment('outcome'))[T.raw_cot]:C(cause)[T.tool_failure]               0.017    0.004   4.248 0.000  0.009  0.025
C(cond, Treatment('outcome'))[T.skill]:C(cause)[T.tool_failure]                -0.000    0.004  -0.072 0.943 -0.008  0.008
model Var                                                                       0.000    0.002                            
task Var                                                                        0.000    0.000                            
==========================================================================================================================

```

## Mixed model: tuse   (crossed variance components: task + model family)

```
                                          Mixed Linear Model Regression Results
==========================================================================================================================
Model:                                   MixedLM                       Dependent Variable:                       tuse     
No. Observations:                        3360                          Method:                                   REML     
No. Groups:                              1                             Scale:                                    0.0004   
Min. group size:                         3360                          Log-Likelihood:                           8370.4641
Max. group size:                         3360                          Converged:                                Yes      
Mean group size:                         3360.0                                                                           
--------------------------------------------------------------------------------------------------------------------------
                                                                               Coef.  Std.Err.    z    P>|z| [0.025 0.975]
--------------------------------------------------------------------------------------------------------------------------
Intercept                                                                       0.037    0.004   9.514 0.000  0.029  0.044
C(cond, Treatment('outcome'))[T.graph]                                         -0.010    0.002  -4.185 0.000 -0.015 -0.005
C(cond, Treatment('outcome'))[T.graph_masked]                                  -0.003    0.002  -1.299 0.194 -0.008  0.002
C(cond, Treatment('outcome'))[T.graph_rule]                                    -0.037    0.002 -15.085 0.000 -0.042 -0.032
C(cond, Treatment('outcome'))[T.raw]                                            0.006    0.002   2.254 0.024  0.001  0.010
C(cond, Treatment('outcome'))[T.raw_cot]                                        0.004    0.002   1.521 0.128 -0.001  0.009
C(cond, Treatment('outcome'))[T.skill]                                         -0.009    0.002  -3.735 0.000 -0.014 -0.004
C(cause)[T.out_of_specialty]                                                    0.009    0.002   3.492 0.000  0.004  0.013
C(cause)[T.persistent_reasoning]                                               -0.030    0.002 -12.129 0.000 -0.034 -0.025
C(cause)[T.tool_failure]                                                        0.000    0.002   0.028 0.977 -0.005  0.005
C(cond, Treatment('outcome'))[T.graph]:C(cause)[T.out_of_specialty]            -0.032    0.003  -9.185 0.000 -0.039 -0.025
C(cond, Treatment('outcome'))[T.graph_masked]:C(cause)[T.out_of_specialty]     -0.033    0.003  -9.524 0.000 -0.040 -0.026
C(cond, Treatment('outcome'))[T.graph_rule]:C(cause)[T.out_of_specialty]       -0.009    0.003  -2.469 0.014 -0.015 -0.002
C(cond, Treatment('outcome'))[T.raw]:C(cause)[T.out_of_specialty]               0.007    0.003   2.116 0.034  0.001  0.014
C(cond, Treatment('outcome'))[T.raw_cot]:C(cause)[T.out_of_specialty]           0.007    0.003   1.913 0.056 -0.000  0.013
C(cond, Treatment('outcome'))[T.skill]:C(cause)[T.out_of_specialty]            -0.036    0.003 -10.382 0.000 -0.043 -0.029
C(cond, Treatment('outcome'))[T.graph]:C(cause)[T.persistent_reasoning]         0.003    0.003   0.869 0.385 -0.004  0.010
C(cond, Treatment('outcome'))[T.graph_masked]:C(cause)[T.persistent_reasoning] -0.003    0.003  -0.766 0.444 -0.009  0.004
C(cond, Treatment('outcome'))[T.graph_rule]:C(cause)[T.persistent_reasoning]    0.040    0.003  11.591 0.000  0.033  0.047
C(cond, Treatment('outcome'))[T.raw]:C(cause)[T.persistent_reasoning]           0.002    0.003   0.605 0.545 -0.005  0.009
C(cond, Treatment('outcome'))[T.raw_cot]:C(cause)[T.persistent_reasoning]       0.004    0.003   1.268 0.205 -0.002  0.011
C(cond, Treatment('outcome'))[T.skill]:C(cause)[T.persistent_reasoning]         0.003    0.003   0.872 0.383 -0.004  0.010
C(cond, Treatment('outcome'))[T.graph]:C(cause)[T.tool_failure]                 0.012    0.003   3.574 0.000  0.006  0.019
C(cond, Treatment('outcome'))[T.graph_masked]:C(cause)[T.tool_failure]          0.008    0.003   2.361 0.018  0.001  0.015
C(cond, Treatment('outcome'))[T.graph_rule]:C(cause)[T.tool_failure]           -0.000    0.003  -0.020 0.984 -0.007  0.007
C(cond, Treatment('outcome'))[T.raw]:C(cause)[T.tool_failure]                   0.014    0.003   4.054 0.000  0.007  0.021
C(cond, Treatment('outcome'))[T.raw_cot]:C(cause)[T.tool_failure]               0.017    0.003   4.994 0.000  0.010  0.024
C(cond, Treatment('outcome'))[T.skill]:C(cause)[T.tool_failure]                -0.000    0.003  -0.084 0.933 -0.007  0.006
model Var                                                                       0.000    0.002                            
task Var                                                                        0.000    0.001                            
==========================================================================================================================

```

## Mixed model: regret   (crossed variance components: task + model family)

```
                                          Mixed Linear Model Regression Results
=========================================================================================================================
Model:                                  MixedLM                       Dependent Variable:                       regret   
No. Observations:                       3360                          Method:                                   REML     
No. Groups:                             1                             Scale:                                    0.0015   
Min. group size:                        3360                          Log-Likelihood:                           5976.1054
Max. group size:                        3360                          Converged:                                Yes      
Mean group size:                        3360.0                                                                           
-------------------------------------------------------------------------------------------------------------------------
                                                                               Coef.  Std.Err.   z    P>|z| [0.025 0.975]
-------------------------------------------------------------------------------------------------------------------------
Intercept                                                                       0.030    0.005  6.052 0.000  0.020  0.040
C(cond, Treatment('outcome'))[T.graph]                                         -0.012    0.005 -2.364 0.018 -0.022 -0.002
C(cond, Treatment('outcome'))[T.graph_masked]                                  -0.001    0.005 -0.170 0.865 -0.011  0.009
C(cond, Treatment('outcome'))[T.graph_rule]                                    -0.030    0.005 -6.044 0.000 -0.040 -0.020
C(cond, Treatment('outcome'))[T.raw]                                           -0.005    0.005 -1.045 0.296 -0.015  0.005
C(cond, Treatment('outcome'))[T.raw_cot]                                       -0.010    0.005 -2.010 0.044 -0.020 -0.000
C(cond, Treatment('outcome'))[T.skill]                                          0.000    0.005  0.073 0.942 -0.009  0.010
C(cause)[T.out_of_specialty]                                                    0.010    0.005  2.076 0.038  0.001  0.020
C(cause)[T.persistent_reasoning]                                                0.065    0.005 13.053 0.000  0.055  0.075
C(cause)[T.tool_failure]                                                       -0.000    0.005 -0.002 0.998 -0.010  0.010
C(cond, Treatment('outcome'))[T.graph]:C(cause)[T.out_of_specialty]            -0.029    0.007 -4.070 0.000 -0.043 -0.015
C(cond, Treatment('outcome'))[T.graph_masked]:C(cause)[T.out_of_specialty]     -0.037    0.007 -5.280 0.000 -0.051 -0.023
C(cond, Treatment('outcome'))[T.graph_rule]:C(cause)[T.out_of_specialty]       -0.010    0.007 -1.468 0.142 -0.024  0.003
C(cond, Treatment('outcome'))[T.raw]:C(cause)[T.out_of_specialty]              -0.015    0.007 -2.062 0.039 -0.028 -0.001
C(cond, Treatment('outcome'))[T.raw_cot]:C(cause)[T.out_of_specialty]          -0.010    0.007 -1.360 0.174 -0.023  0.004
C(cond, Treatment('outcome'))[T.skill]:C(cause)[T.out_of_specialty]            -0.041    0.007 -5.793 0.000 -0.055 -0.027
C(cond, Treatment('outcome'))[T.graph]:C(cause)[T.persistent_reasoning]        -0.018    0.007 -2.479 0.013 -0.031 -0.004
C(cond, Treatment('outcome'))[T.graph_masked]:C(cause)[T.persistent_reasoning] -0.006    0.007 -0.891 0.373 -0.020  0.008
C(cond, Treatment('outcome'))[T.graph_rule]:C(cause)[T.persistent_reasoning]   -0.048    0.007 -6.812 0.000 -0.062 -0.034
C(cond, Treatment('outcome'))[T.raw]:C(cause)[T.persistent_reasoning]          -0.001    0.007 -0.207 0.836 -0.015  0.012
C(cond, Treatment('outcome'))[T.raw_cot]:C(cause)[T.persistent_reasoning]       0.004    0.007  0.606 0.545 -0.010  0.018
C(cond, Treatment('outcome'))[T.skill]:C(cause)[T.persistent_reasoning]        -0.008    0.007 -1.140 0.254 -0.022  0.006
C(cond, Treatment('outcome'))[T.graph]:C(cause)[T.tool_failure]                 0.009    0.007  1.212 0.226 -0.005  0.022
C(cond, Treatment('outcome'))[T.graph_masked]:C(cause)[T.tool_failure]          0.007    0.007  1.021 0.307 -0.007  0.021
C(cond, Treatment('outcome'))[T.graph_rule]:C(cause)[T.tool_failure]            0.000    0.007  0.001 0.999 -0.014  0.014
C(cond, Treatment('outcome'))[T.raw]:C(cause)[T.tool_failure]                   0.003    0.007  0.393 0.694 -0.011  0.017
C(cond, Treatment('outcome'))[T.raw_cot]:C(cause)[T.tool_failure]               0.012    0.007  1.648 0.099 -0.002  0.025
C(cond, Treatment('outcome'))[T.skill]:C(cause)[T.tool_failure]                -0.000    0.007 -0.030 0.976 -0.014  0.014
model Var                                                                       0.000    0.000                           
task Var                                                                        0.000    0.003                           
=========================================================================================================================

```

## McNemar (exact): binary 'correct delegation decision on both same-skill probes' (paired by episode x seed x model)

| contrast | b (A right, B wrong) | c (A wrong, B right) | p |
|---|---|---|---|
| graph vs outcome | 383 | 67 | 7.52e-55 |
| graph vs skill | 222 | 52 | 3.48e-26 |
| graph vs raw | 259 | 118 | 2.96e-13 |
| graph vs raw_cot | 248 | 113 | 9.59e-13 |
| graph_masked vs outcome | 243 | 114 | 7.44e-12 |
| graph_masked vs skill | 93 | 110 | 2.61e-01 |
| graph_masked vs raw | 129 | 175 | 9.74e-03 |
| graph_masked vs raw_cot | 129 | 181 | 3.70e-03 |
| graph_rule vs outcome | 825 | 0 | 8.94e-249 |
| graph_rule vs skill | 679 | 0 | 7.97e-205 |
| graph_rule vs raw | 663 | 13 | 5.73e-177 |
| graph_rule vs raw_cot | 652 | 8 | 3.62e-181 |

## Robustness across model families (per-model means; graph vs baselines)

| model | condition | TCE | TUSE | regret | FCSR |
|---|---|---|---|---|---|
| openai/gpt-4o-mini | outcome | 0.067 | 0.029 | 0.047 | 0.136 |
| openai/gpt-4o-mini | skill | 0.048 | 0.014 | 0.036 | 0.127 |
| openai/gpt-4o-mini | raw | 0.083 | 0.053 | 0.042 | 0.107 |
| openai/gpt-4o-mini | raw_cot | 0.087 | 0.057 | 0.044 | 0.103 |
| openai/gpt-4o-mini | graph_masked | 0.063 | 0.030 | 0.038 | 0.111 |
| openai/gpt-4o-mini | graph | 0.072 | 0.023 | 0.035 | 0.101 |
| openai/gpt-4o-mini | graph_rule | 0.024 | 0.002 | 0.004 | 0.094 |
| anthropic/claude-haiku-5.5 | outcome | 0.067 | 0.029 | 0.059 | 0.139 |
| anthropic/claude-haiku-5.5 | skill | 0.052 | 0.017 | 0.044 | 0.130 |
| anthropic/claude-haiku-5.5 | raw | 0.059 | 0.033 | 0.040 | 0.132 |
| anthropic/claude-haiku-5.5 | raw_cot | 0.056 | 0.026 | 0.036 | 0.149 |
| anthropic/claude-haiku-5.5 | graph_masked | 0.048 | 0.013 | 0.043 | 0.146 |
| anthropic/claude-haiku-5.5 | graph | 0.038 | 0.006 | 0.022 | 0.127 |
| anthropic/claude-haiku-5.5 | graph_rule | 0.025 | 0.003 | 0.006 | 0.147 |
| meta-llama/llama-3.3-70b-instruct | outcome | 0.068 | 0.036 | 0.042 | 0.115 |
| meta-llama/llama-3.3-70b-instruct | skill | 0.045 | 0.011 | 0.032 | 0.122 |
| meta-llama/llama-3.3-70b-instruct | raw | 0.069 | 0.043 | 0.040 | 0.100 |
| meta-llama/llama-3.3-70b-instruct | raw_cot | 0.070 | 0.044 | 0.042 | 0.096 |
| meta-llama/llama-3.3-70b-instruct | graph_masked | 0.051 | 0.021 | 0.036 | 0.113 |
| meta-llama/llama-3.3-70b-instruct | graph | 0.055 | 0.022 | 0.026 | 0.099 |
| meta-llama/llama-3.3-70b-instruct | graph_rule | 0.022 | 0.003 | 0.003 | 0.122 |

Sign-consistency check: for each model, does graph beat outcome AND skill on TCE and regret?

- openai/gpt-4o-mini: NO
- anthropic/claude-haiku-5.5: YES
- meta-llama/llama-3.3-70b-instruct: NO