import nibabel as nib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


#create combined surf.gii for plotting
    
template_gii='hippomaps/resources/canonical_surfs/tpl-avg_space-{space}_den-{density}_label-{label}_{surf}.surf.gii'
hipp_curv_nii='hippomaps/resources/parc-multihist7/curvature.nii.gz'
subfield_lut = {'Subiculum':1, 'CA1': 2,'CA2': 3, 'CA3': 4, 'CA4': 5, 'DG': 6}
out_surf_gii = 'tpl-avg_hemi-{hemi}_space-{space}_label-{label}_density-{density}_{surf}.surf.gii'

hemis=['left','right']
surfs=['midthickness']
densities= ['unfoldiso','0p5mm','1mm','2mm']
spaces = ['canonical','unfold']

for hemi in hemis:
    for surf in surfs:
        for density in densities:
            for space in spaces:
                print(f'{hemi}, {space}')
                template_gii_nib = nib.load(template_gii.format(density=density,space=space,label=labels[0],surf=surf))
                faces = {}
                points = {}
                for label in labels:
                    faces[label] = nib.load(template_gii.format(density=density,space=space,label=label,surf=surf)).darrays[0].data
                    points[label] = nib.load(template_gii.format(density=density,space=space,label=label,surf=surf)).darrays[1].data

                #now, to put them in the same surface, we concatenate them making sure to offset the indices (faces) 
                faces['dentate'] = faces['dentate'] + points['hipp'].shape[0]
                faces['merged'] = np.vstack((faces['hipp'],faces['dentate']))
                
                #translate dentate to the other side of unfolded hipp
                if space == 'unfold':
                    points['dentate'][:,1] = points['dentate'][:,1] + 22
                points['merged'] = np.vstack((points['hipp'],points['dentate']))
                
                
                if hemi == 'left':
                    points['merged'] = -1 * points['merged']
                
                if hemi == 'right' and space == 'unfold':
                    points['merged'][:,0] = -1 * points['merged'][:,0]
                
                
                if space == 'canonical':
                    if hemi == 'left':
                        rotated_points = rotate_points(points['merged'],elev=180,azim=0,roll=90)

                
                        points['merged'] = rotated_points
                    elif hemi == 'right':
                        rotated_points = rotate_points(points['merged'],elev=0,azim=0,roll=90)
                        points['merged'] = rotated_points

                
                                
                tri_darray = nib.gifti.GiftiDataArray(
                    data=faces['merged'], intent="NIFTI_INTENT_TRIANGLE", datatype="NIFTI_TYPE_INT32"
                )
                
                points_darray = nib.gifti.GiftiDataArray(
                    data=points['merged'], intent="NIFTI_INTENT_POINTSET", datatype="NIFTI_TYPE_FLOAT32"
                )
                
                out_nib = nib.GiftiImage()
                out_nib.add_gifti_data_array(tri_darray)
                out_nib.add_gifti_data_array(points_darray)
                out_nib.to_filename(out_surf_gii.format(hemi=hemi,space=space,density=density,label='hippdentate',surf=surf))


#create combined surf.gii for plotting
    

out_curv_gii = 'tpl-avg_label-{label}_density-{density}_curvature.shape.gii'

    
#make bg_map using hipp curvature (
hipp_curv_vol = nib.load(hipp_curv_nii).get_fdata()
hipp_curv_unfoldiso = hipp_curv_vol.T.reshape((np.prod(hipp_curv_vol.shape),))


for density in densities:

    #load gifti to get shape
    ref_gii_nib = nib.load(out_surf_gii.format(hemi=hemis[0],space=spaces[0],label='hippdentate',surf='midthickness',density=density))
    
    
    
    if density == 'unfoldiso':
        hipp_curv = hipp_curv_unfoldiso
    else:
        hipp_curv,_,_ = density_interp('unfoldiso',density,hipp_curv_unfoldiso,label='hipp',method='linear')
               
    hippdentate_curv = np.zeros((ref_gii_nib.darrays[1].data.shape[0],))
    hippdentate_curv[:hipp_curv.shape[0]] = hipp_curv
    
    curv = nib.gifti.GiftiDataArray(
        data=hippdentate_curv, intent="NIFTI_INTENT_SHAPE", datatype="NIFTI_TYPE_FLOAT32"
    )
    
    
    out_nib = nib.GiftiImage()
    out_nib.add_gifti_data_array(curv)
    out_nib.to_filename(out_curv_gii.format(density=density,label='hippdentate'))



#write subfields to gifti
from nibabel.gifti import GiftiLabel, GiftiLabelTable

def get_hippdentate_labels(density='0p5mm'):
    space='canonical'
    template_gii='hippomaps/resources/canonical_surfs/tpl-avg_space-{space}_den-{density}_label-{label}_{surf}.surf.gii'
    label_gii='hippomaps/resources/parc-multihist7/sub-0_hemi-0_space-0_den-{density}_label-hipp_atlas-multihist7_subfields.label.gii'
    subfield_lut = {'Subiculum':1, 'CA1': 2,'CA2': 3, 'CA3': 4, 'CA4': 5, 'DG': 6}

    points_merged =  nib.load(out_surf_gii.format(hemi=hemis[0],density=density,space=space,label='hippdentate',surf='midthickness')).get_arrays_from_intent('NIFTI_INTENT_POINTSET')[0].data
    n_total = points_merged.shape[0]
    
    subfields_hipp = nib.load(label_gii.format(density=density)).agg_data()

    n_hipp = subfields_hipp.shape[0]
    subfields = np.zeros((n_total,1)) 
    
    subfields[:n_hipp,0] = subfields_hipp
    subfields[n_hipp:,0] = subfield_lut['DG'] #rest of them become dentate 

    return subfields
    

out_label_gii = 'tpl-avg_label-{label}_density-{density}_subfields.label.gii'

# Define labels from labellist.txt
labellist = [
    {"name": "Subiculum", "index": 1, "rgba": [0, 0, 255, 255]},
    {"name": "CA1", "index": 2, "rgba": [133, 222, 255, 255]},
    {"name": "CA2", "index": 3, "rgba": [0, 255, 170, 255]},
    {"name": "CA3", "index": 4, "rgba": [255, 162, 0, 255]},
    {"name": "CA4", "index": 5, "rgba": [255, 0, 0, 255]},
    {"name": "DG", "index": 6, "rgba": [255, 255, 0, 255]},
]


# Create a label table
label_table = GiftiLabelTable()
for label in labellist:
    gifti_label = GiftiLabel(
        key=label["index"],
        red=label["rgba"][0],
        green=label["rgba"][1],
        blue=label["rgba"][2],
        alpha=label["rgba"][3],
    )
    gifti_label.label = label["name"]  # Set the name of the label
    label_table.labels.append(gifti_label)

for density in densities:
    subfield_labels = get_hippdentate_labels(density)


    label_darray = nib.gifti.GiftiDataArray(
        data=subfield_labels, intent="NIFTI_INTENT_SHAPE", datatype="NIFTI_TYPE_INT32"
    )
    
    # Attach label table to a new GIFTI image    
    out_nib = nib.GiftiImage()
    out_nib.add_gifti_data_array(label_darray)
    out_nib.labeltable = label_table

    out_nib.to_filename(out_label_gii.format(density=density,label='hippdentate'))



