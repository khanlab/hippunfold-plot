

# examples
```
label_gii = 'tpl-avg_label-hippdentate_density-{density}_subfields.label.gii'

density='1mm'
fig = plot_hippdentate(label_gii.format(density=density),hemi=None,density=density,view='dorsal')
fig = plot_hippdentate(label_gii.format(density=density), hemi=None,density=density,view='ventral')
```


```
fig = plot_hippdentate(label_gii.format(density=density),hemi='left',density=density,view='dorsal')
fig.show()
fig = plot_hippdentate(label_gii.format(density=density),hemi='right',density=density,view='dorsal')
fig.show()
```


```
fig = plot_hippdentate(label_gii.format(density=density),space='unfold',hemi='left',density=density,view='dorsal')
fig.show()
fig = plot_hippdentate(label_gii.format(density=density),space='unfold',hemi='right',density=density,view='dorsal')
fig.show()
```

