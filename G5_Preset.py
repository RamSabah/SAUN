#Preset Class for Solution 5


P1 = ["hasAxis","hasDepth","hasMaxDepth","hasMinDepth","hasDiameter","hasMaxDiameter","hasMinDiameter","hasHeight","hasMaxHeight","hasMinHeight",
      "hasWidth","hasMaxWidth","hasMinWidth","hasWeight","hasWeightStandard","hasBearsDate","hasEndDate","hasStartDate","hasDenomination"]
P2 = ["hasCollection","hasTypeSeriesItem"]
P3 = ["hasContemporaryName","hasScholarlyName"]
P4 = ["hasDie","hasProductionObject","hasManufacture"]
P5 = ["hasCountermark","hasMintmark","hasSecondaryTreatment","hasPeculiarity","hasPeculiarityOfProduction","hasCorrosion","hasWear"]

P6 = ["hasObjectType","representsObjectType"]
P7 = ["hasAuthenticity"]
P8 = ["hasAuthority","hasIssuer"]
P9 = ["hasMint","hasFindspot"]
P10 = ["hasMaterial"]
P11 = ["hasContext"]
P12 = ["hasAppearance","hasShape","hasEdge"]
P13 = ["hasFace","hasObverse","hasReverse"]
P14 = ["hasPortrait","hasIconography","hasLegend"]
Base = ["P3_uncertain_value","P107_uncertain_member",
        "P102_uncertain_name_or_ethnic","P16.2_uncertain_technique_or_object_used_for_creation",
          "P103.2_uncertain_symbole_or_features","P67.2_uncertain_type","P138.2_uncertain_authenticity",
        "P14_uncertain_authority_or_issuer",
          "P189.2_uncertain_place",
        "P137_uncertain_material",
        "P136_uncertain_context_or_taxonomy",
        "P139_uncertain_form","P19_uncertain_mode",
        "P62_uncertain_depiction"]
all = [P1,P2,P3,P4,P5,P6,P7,P8,P9,P10,P11,P12,P13,P14]
def getLiteral(element):
    for i in range(len(all)):
        for j in range(len(all[i])):
            if all[i][j] == element:
                return Base[i]
    print(element," is in the Loop")



