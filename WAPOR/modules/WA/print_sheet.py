# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 12:11:04 2016

@author: bec
"""


import os
import cairosvg
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET



def scale_factor(scale_test):
    scale = 0
    while np.all([scale_test < 10.000, scale_test != 0.0]):
        scale_test *= 10
        scale += 1
    scale = float(np.min([2,scale]))
    return scale


def create_sheet_png(basin, period, units, data, output, template=False , smart_unit = False):
    """

    Keyword arguments:
    basin -- The name of the basin
    period -- The period of analysis
    units -- The units of the data
    data -- A csv file that contains the water data. The csv file has to
            follow an specific format. A sample csv is available in the link:
            https://github.com/wateraccounting/wa/tree/master/Sheets/csv
    output -- The output path of the jpg file for the sheet.
    template -- A svg file of the sheet. Use False (default) to use the
                standard svg file.

    Example:
    from wa.Sheets import *
    create_sheet1(basin='Incomati', period='2005-2010', units='km3/year',
                  data=r'C:\Sheets\csv\Sample_sheet1.csv',
                  output=r'C:\Sheets\sheet_1.jpg')
    """
   # decimals = 1
    # Read table

    df = pd.read_csv(data, sep=';')
    
    scale = 0
    if smart_unit:
        scale_test = np.nanmax(df['VALUE'].values)
        scale = scale_factor(scale_test)
        df['VALUE'] *= 10**scale

    # Data frames

    df_i = df.loc[df.CLASS == "INFLOW"]
    df_s = df.loc[df.CLASS == "STORAGE"]
    df_o = df.loc[df.CLASS == "OUTFLOW"]

    # Inflow data

    rainfall = float(df_i.loc[(df_i.SUBCLASS == "PRECIPITATION") &
                              (df_i.VARIABLE == "Rainfall")].VALUE)
    snowfall = float(df_i.loc[(df_i.SUBCLASS == "PRECIPITATION") &
                              (df_i.VARIABLE == "Snowfall")].VALUE)
    p_recy = float(df_i.loc[(df_i.SUBCLASS == "PRECIPITATION") &
                   (df_i.VARIABLE == "Precipitation recycling")].VALUE)

    sw_mrs_i = float(df_i.loc[(df_i.SUBCLASS == "SURFACE WATER") &
                              (df_i.VARIABLE == "Main riverstem")].VALUE)
    sw_tri_i = float(df_i.loc[(df_i.SUBCLASS == "SURFACE WATER") &
                              (df_i.VARIABLE == "Tributaries")].VALUE)
    sw_usw_i = float(df_i.loc[(df_i.SUBCLASS == "SURFACE WATER") &
                     (df_i.VARIABLE == "Utilized surface water")].VALUE)
    sw_flo_i = float(df_i.loc[(df_i.SUBCLASS == "SURFACE WATER") &
                              (df_i.VARIABLE == "Flood")].VALUE)

    gw_nat_i = float(df_i.loc[(df_i.SUBCLASS == "GROUNDWATER") &
                              (df_i.VARIABLE == "Natural")].VALUE)
    gw_uti_i = float(df_i.loc[(df_i.SUBCLASS == "GROUNDWATER") &
                              (df_i.VARIABLE == "Utilized")].VALUE)

    q_desal = float(df_i.loc[(df_i.SUBCLASS == "OTHER") &
                             (df_i.VARIABLE == "Desalinized")].VALUE)

    # Storage data

    surf_sto = float(df_s.loc[(df_s.SUBCLASS == "CHANGE") &
                              (df_s.VARIABLE == "Surface storage")].VALUE)
    sto_sink = float(df_s.loc[(df_s.SUBCLASS == "CHANGE") &
                              (df_s.VARIABLE == "Storage in sinks")].VALUE)

    # Outflow data

    et_l_pr = float(df_o.loc[(df_o.SUBCLASS == "ET LANDSCAPE") &
                             (df_o.VARIABLE == "Protected")].VALUE)
    et_l_ut = float(df_o.loc[(df_o.SUBCLASS == "ET LANDSCAPE") &
                             (df_o.VARIABLE == "Utilized")].VALUE)
    et_l_mo = float(df_o.loc[(df_o.SUBCLASS == "ET LANDSCAPE") &
                             (df_o.VARIABLE == "Modified")].VALUE)
    et_l_ma = float(df_o.loc[(df_o.SUBCLASS == "ET LANDSCAPE") &
                             (df_o.VARIABLE == "Managed")].VALUE)

    et_u_pr = float(df_o.loc[(df_o.SUBCLASS == "ET UTILIZED FLOW") &
                             (df_o.VARIABLE == "Protected")].VALUE)
    et_u_ut = float(df_o.loc[(df_o.SUBCLASS == "ET UTILIZED FLOW") &
                             (df_o.VARIABLE == "Utilized")].VALUE)
    et_u_mo = float(df_o.loc[(df_o.SUBCLASS == "ET UTILIZED FLOW") &
                             (df_o.VARIABLE == "Modified")].VALUE)

    et_u_ma = float(df_o.loc[(df_o.SUBCLASS == "ET UTILIZED FLOW") &
                             (df_o.VARIABLE == "Managed")].VALUE)

    et_manmade = float(df_o.loc[(df_o.SUBCLASS == "ET INCREMENTAL") &
                                (df_o.VARIABLE == "Manmade")].VALUE)
    et_natural = float(df_o.loc[(df_o.SUBCLASS == "ET INCREMENTAL") &
                                (df_o.VARIABLE == "Natural")].VALUE)

    sw_mrs_o = float(df_o.loc[(df_o.SUBCLASS == "SURFACE WATER") &
                              (df_o.VARIABLE == "Main riverstem")].VALUE)
    sw_tri_o = float(df_o.loc[(df_o.SUBCLASS == "SURFACE WATER") &
                              (df_o.VARIABLE == "Tributaries")].VALUE)
    sw_usw_o = float(df_o.loc[(df_o.SUBCLASS == "SURFACE WATER") &
                     (df_o.VARIABLE == "Utilized surface water")].VALUE)
    sw_flo_o = float(df_o.loc[(df_o.SUBCLASS == "SURFACE WATER") &
                              (df_o.VARIABLE == "Flood")].VALUE)

    gw_nat_o = float(df_o.loc[(df_o.SUBCLASS == "GROUNDWATER") &
                              (df_o.VARIABLE == "Natural")].VALUE)
    gw_uti_o = float(df_o.loc[(df_o.SUBCLASS == "GROUNDWATER") &
                              (df_o.VARIABLE == "Utilized")].VALUE)

    basin_transfers = float(df_o.loc[(df_o.SUBCLASS == "SURFACE WATER") &
                            (df_o.VARIABLE == "Interbasin transfer")].VALUE)
    non_uti = float(df_o.loc[(df_o.SUBCLASS == "OTHER") &
                             (df_o.VARIABLE == "Non-utilizable")].VALUE)
    other_o = float(df_o.loc[(df_o.SUBCLASS == "OTHER") &
                             (df_o.VARIABLE == "Other")].VALUE)

    com_o = float(df_o.loc[(df_o.SUBCLASS == "RESERVED") &
                           (df_o.VARIABLE == "Commited")].VALUE)
    nav_o = float(df_o.loc[(df_o.SUBCLASS == "RESERVED") &
                           (df_o.VARIABLE == "Navigational")].VALUE)
    env_o = float(df_o.loc[(df_o.SUBCLASS == "RESERVED") &
                           (df_o.VARIABLE == "Environmental")].VALUE)

    # Calculations & modify svg
    if not template:
        path = os.path.dirname(os.path.abspath(__file__))
        svg_template_path = os.path.join(path, 'svg', 'sheet_1_hydro.svg')
    else:
        svg_template_path = os.path.abspath(template)

    tree = ET.parse(svg_template_path)

    # Titles

    xml_txt_box = tree.findall('''.//*[@id='basin']''')[0]
    list(xml_txt_box)[0].text = 'Basin: ' + basin

    xml_txt_box = tree.findall('''.//*[@id='period']''')[0]
    list(xml_txt_box)[0].text = 'Period: ' + period

    xml_txt_box = tree.findall('''.//*[@id='units']''')[0]
    
    if np.all([smart_unit, scale > 0]):
        list(xml_txt_box)[0].text = 'Sheet 1: Resource Base ({0} {1})'.format(10**-scale, units)
    else:
        list(xml_txt_box)[0].text = 'Sheet 1: Resource Base ({0})'.format(units)

    # Grey box

    p_advec = rainfall + snowfall
    q_sw_in = sw_mrs_i + sw_tri_i + sw_usw_i + sw_flo_i
    q_gw_in = gw_nat_i + gw_uti_i

    external_in = p_advec + q_desal + q_sw_in + q_gw_in
    gross_inflow = external_in + p_recy

    delta_s = surf_sto + sto_sink
    
    # Pink box

    net_inflow = gross_inflow + delta_s
    
    p1 = {
            'external_in' : external_in,
            'p_advec' : p_advec,
            'q_desal' : q_desal,
            'q_sw_in' : q_sw_in,
            'q_gw_in' : q_gw_in,
            'p_recycled' : p_recy,
            'gross_inflow' : gross_inflow,
            'net_inflow' : net_inflow
            }
 
    for key in list(p1.keys()):
        if tree.findall(".//*[@id='{0}']".format(key)) != []:
            xml_txt_box = tree.findall(".//*[@id='{0}']".format(key))[0]
            if not pd.isnull(p1[key]):
                list(xml_txt_box)[0].text = '%.1f' % p1[key]
            else:
               list(xml_txt_box)[0].text = '-'
    
    delta_s_posbox = (delta_s + abs(delta_s))/2
    delta_s_negbox = abs(delta_s - abs(delta_s))/2 
    
    st = {
            'pos_delta_s' : delta_s_posbox,
            'neg_delta_s' : delta_s_negbox
            }

    for key in list(st.keys()):
        if tree.findall(".//*[@id='{0}']".format(key)) != []:
            xml_txt_box = tree.findall(".//*[@id='{0}']".format(key))[0]
            if not pd.isnull(st[key]):
                list(xml_txt_box)[0].text = '%.1f' % st[key]
            else:
               list(xml_txt_box)[0].text = '-'    

    # Light-green box
    land_et = et_l_pr + et_l_ut + et_l_mo + et_l_ma
    
    # landscape et
    landsc_et = land_et + et_u_pr + et_u_ut + et_u_mo #duplicate number, unneeded

    p2 = {
            'landscape_et' : landsc_et,
            'green_protected' : et_l_pr,
            'green_utilized' : et_l_ut,
            'green_modified' : et_l_mo,
            'green_managed' : et_l_ma,
            'rainfall_et' : land_et,
#            'landscape_et' : landsc_et
            }
    
    for key in list(p2.keys()):
        if tree.findall(".//*[@id='{0}']".format(key)) != []:
            xml_txt_box = tree.findall(".//*[@id='{0}']".format(key))[0]
            if not pd.isnull(p2[key]):
                list(xml_txt_box)[0].text = '%.1f' % p2[key]
            else:
               list(xml_txt_box)[0].text = '-'

    # Blue box (center)

    exploitable_water = net_inflow - land_et - et_u_pr - et_u_ut - et_u_mo
    reserved_outflow = max(com_o, nav_o, env_o)

    available_water = exploitable_water - non_uti - reserved_outflow

#    utilized_flow = et_u_pr + et_u_ut + et_u_mo + et_u_ma
    utilized_flow = et_u_ma    
    utilizable_outflow = available_water - utilized_flow

    inc_et = et_manmade + et_natural

    non_cons_water = utilizable_outflow + non_uti + reserved_outflow

    non_rec_flow = et_u_pr + et_u_ut + et_u_mo + et_u_ma - inc_et - other_o
    
    p3 = {
            'incremental_etman' : et_manmade,
            'incremental_etnat' : et_natural,
            'exploitable_water' : exploitable_water,
            'available_water' : available_water,
            'blue_protected' : et_u_pr,
            'blue_utilized' : et_u_ut,
            'blue_modified' : et_u_mo,
            'blue_managed' : et_u_ma,
            'utilizable_outflow' : utilizable_outflow,
            'non-utilizable_outflow' : non_uti,
            'reserved_outflow_max' : reserved_outflow,
            'non-consumed_water' : non_cons_water,
            'non-recoverable_flow' : non_rec_flow
            }

    for key in list(p3.keys()):
        if tree.findall(".//*[@id='{0}']".format(key)) != []:
            xml_txt_box = tree.findall(".//*[@id='{0}']".format(key))[0]
            if not pd.isnull(p3[key]):
                list(xml_txt_box)[0].text = '%.1f' % p3[key]
            else:
               list(xml_txt_box)[0].text = '-'

#    xml_txt_box = tree.findall('''.//*[@id='utilized_flow']''')[0]
#    list(xml_txt_box)[0].text = '{1:.{0}f}'.format(decimals, utilized_flow)

#    xml_txt_box = tree.findall('''.//*[@id='manmade']''')[0]
#    list(xml_txt_box)[0].text = '{1:.{0}f}'.format(decimals, et_manmade)
#
#    xml_txt_box = tree.findall('''.//*[@id='natural']''')[0]
#    list(xml_txt_box)[0].text = '{1:.{0}f}'.format(decimals, et_natural)

#    xml_txt_box = tree.findall('''.//*[@id='other']''')[0]
#    list(xml_txt_box)[0].text = '{1:.{0}f}'.format(decimals, other_o)


    # Blue box (right)

    outflow = non_cons_water + non_rec_flow 

    q_sw_out = sw_mrs_o + sw_tri_o + sw_usw_o + sw_flo_o 
    q_gw_out = gw_nat_o + gw_uti_o
    
    # Dark-green box
    consumed_water = landsc_et + utilized_flow
    depleted_water = consumed_water - p_recy - non_rec_flow
    external_out = depleted_water + outflow
    
    p4 = {
            'outflow' : outflow,
            'q_sw_outlet' : q_sw_out,
            'q_sw_out' : basin_transfers,
            'q_gw_out' : q_gw_out,
            'et_recycled' : p_recy,
            'consumed_water' : consumed_water,
            'depleted_water' : depleted_water,
            'external_out' : external_out,
            'et_out' : depleted_water
            }

    for key in list(p4.keys()):
        if tree.findall(".//*[@id='{0}']".format(key)) != []:
            xml_txt_box = tree.findall(".//*[@id='{0}']".format(key))[0]
            if not pd.isnull(p4[key]):
                list(xml_txt_box)[0].text = '%.1f' % p4[key]
            else:
               list(xml_txt_box)[0].text = '-'

#    # Export svg to pdf
    tempout_path = output.replace('.pdf', '_temporary.svg')
    tree.write(tempout_path)    
    cairosvg.svg2pdf(url=tempout_path, write_to=output)    
    os.remove(tempout_path)
    # Return
    return output

