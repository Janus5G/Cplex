# CPL support

Cplex understøtter aktuelt to CPL-spor.

## Simple-CPL

Simple-CPL kommer fra chromaplex_os.

Eksempel:

var x = 1000;  
store x at (10, 20, 30) colour GREEN;  
load y from (10, 20, 30) colour GREEN;  
print y;

Dette spor kan bygges som legacy .bin.

## Dansk CPL

Dansk CPL kommer fra chromaplex.

Eksempel:

konstant BREDDE = 10  
konstant HOEJDE = 10

for y = 0 to HOEJDE-1 {  
    for x = 0 to BREDDE-1 {  
        pixel pixeldata = hent_pixel(x, y)

        potens r_e, rest r_rest = komponent_til_potens(pixeldata.rød)

        skriv_voxel(x, y, 0) {  
            kanal rød = r_e, rest = r_rest;  
        }  
    }  
}

Dette spor kompileres til CPA assembly og kan bygges som CPA bundle.

## Aktuelt understøttet dansk CPL

Cplex understøtter blandt andet:

- konstant
- simple compile-time for-loops
- pixel hent_pixel(x, y)
- komponent_til_potens(...)
- potens_til_tal(...)
- skriv_voxel(...)
- kanal rød/grøn/blå/violet/uv
- læs_voxel(...)
- opret_hologram(...)
- hologram.sæt_pixel(...)
- vis_hologram(hologram)

Nogle dele er stadig demo-/compile-time-understøttelse og skal senere gøres til rigtig runtime-semantik.
