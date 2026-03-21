# python Example

```
import geopandas as gpd
import numpy as np
from shapely.geometry import box

def spatial_block_split(gdf, n_blocks_per_side=5, test_fraction=0.2):
    """Assign samples to spatial grid blocks; hold out entire blocks as test."""
    bounds = gdf.total_bounds  # [minx, miny, maxx, maxy]
    bw = (bounds[2] - bounds[0])
    bh = (bounds[3] - bounds[1])

    blocks = []
    for i in range(n_blocks_per_side):
        for j in range(n_blocks_per_side):
            b = box(bounds[0]+i*bw, bounds[1]+j*bh,
                    bounds[0]+(i+1)*bw, bounds[1]+(j+1)*bh)
            blocks.append({'block_id': i*n_blocks_per_side+j, 'geometry': b})

    blocks_gdf = gpd.GeoDataFrame(blocks, crs=gdf.crs)
    gdf = gpd.sjoin(gdf, blocks_gdf, how='left')

    unique_blocks = gdf['block_id'].unique()
    n_test = max(1, int(len(unique_blocks) * test_fraction))
    test_blocks = np.random.choice(unique_blocks, n_test, replace=False)

    return gdf[~gdf['block_id'].isin(test_blocks)], gdf[gdf['block_id'].isin(test_blocks)]
```
