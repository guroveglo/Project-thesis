if __name__ == '__main__':

    import seacharts

    #size = 9000, 5062                # w, h (east, north) distance in meters
    #center = 44300, 6956450          # easting/northing (UTM zone 33N)
    #files = ['Basisdata_46_Vestland_25833_Dybdedata_FGDB.gdb']  # Norwegian county database name
    #files = ['Basisdata_15_More_og_Romsdal_25833_Dybdedata_FGDB.gdb']
    #enc = seacharts.ENC(size=size, center=center, files=files, new_data=True)

    enc = seacharts.ENC(new_data=False)

    print(enc.seabed[10])
    print(enc.shore)
    print(enc.land)