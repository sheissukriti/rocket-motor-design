#FINAL CODES

#all units are in mm

#HIGH FOZ NOZZLE
import cadquery as cq
import math


def generate_cad_files(rocket_dimensions):
    cd_nozzle(rocket_dimensions['nozzle_throat_diam'], rocket_dimensions['nozzle_exit_diam'], rocket_dimensions['nozzle_inlet_diam'], rocket_dimensions['nozzle_outer_diam'], rocket_dimensions['nozzle_convergent_angle'], rocket_dimensions['nozzle_divergent_angle'], rocket_dimensions['nozzle_a'], rocket_dimensions['nozzle_b'])
    motor_casing(rocket_dimensions['casing_outer_diameter'], rocket_dimensions['casing_inner_diameter'], rocket_dimensions['casing_height'])
    bates_grain(rocket_dimensions['grain_outer_diameter'], rocket_dimensions['grain_inner_diameter'], rocket_dimensions['grain_height'])
    bulkhead_generic(rocket_dimensions['bulkhead_hole_diameter'], rocket_dimensions['bulkhead_outer_diameter'], rocket_dimensions['bulkhead_thickness'], rocket_dimensions['bulkhead_height'], rocket_dimensions['bulkhead_a'], rocket_dimensions['bulkhead_b'])
    return True
def cd_nozzle(throat_diam, exit_diam, inlet_diam, outer_diam, conv_angle, div_angle,a,b):

    #a = o ring height
    #b = o ring width

    re = (exit_diam/2)#exit radius
    rt = (throat_diam/2)#throat radius
    ri = (inlet_diam/2)#inlet radius
    ro = (outer_diam/2)#outer nozzle radius
    theta_d = math.tan(math.radians(div_angle))#divergent angle formula
    theta_c = math.tan(math.radians(conv_angle))#convergent angle formula

    h = (re - rt)/(theta_d)
    x = (ri-rt)/(theta_c)

    nozzle = (
        cq.Workplane('XY')
        .center(-re,0)
        .moveTo(-re,0)
        .lineTo(-rt,h)
        .lineTo(-ri,h+x)
        .lineTo(-ro,h+x)
        .lineTo(-ro,h+(a/2))
        .lineTo(-ro+b,(h+(a/2)))
        .lineTo(-ro+b,(h-(a/2)))
        .lineTo(-ro,(h-(a/2)))
        .lineTo(-ro,0)
        .lineTo(-re,0)
        .close()
        
    )
    nozzle_3d = nozzle.revolve(angleDegrees=360, axisStart=(0, 0, 0), axisEnd=(0,1000,0))
    nozzle_3d.export("nozzle.stl")
    return nozzle_3d

#overhang nozzle

def overhang_nozzle(throat_diam, exit_diam, inlet_diam, wall_thick, conv_angle, div_angle, lc):
    #lc = chamber length
    re = exit_diam / 2  # Exit radius
    rt = throat_diam / 2  # Throat radius
    ri = inlet_diam / 2  # Inlet radius
    
    # Calculate angles in radians
    theta_d = math.tan(math.radians(div_angle))  # Divergent angle
    theta_c = math.tan(math.radians(conv_angle))  # Convergent angle

    # Calculate lengths of divergent/convergent sections
    h = (re - rt) / theta_d  # Divergent section length
    x = (ri - rt) / theta_c  # Convergent section length

    o_nozzle = (
        cq.Workplane('XY')
        .center(-re,0)
        .moveTo(-re,0)
        .lineTo(-rt,h)
        .lineTo(-ri,h+x)
        .lineTo(-ri,h+x+lc)
        .lineTo(-ri-wall_thick,h+x+lc)
        .lineTo(-ri-wall_thick,h+x)
        .lineTo(-rt-wall_thick,h)
        .lineTo(-ri-wall_thick,0)
        .lineTo(-re,0)
        .close()
        
    )
    o_nozzle_3d = (
        o_nozzle.revolve(angleDegrees=360, axisStart=(0, 0, 0), axisEnd=(0, 1000, 0))
    )
    o_nozzle_3d.export("overhang_nozzle.stl")
    return o_nozzle_3d




#MOTOR CASING

def motor_casing(outer_diam, inner_diam, extr_height):
    ro = outer_diam / 2  # Outer radius
    ri = inner_diam / 2  # Inner radius

    casing = (
        cq.Workplane('top')
        .circle(ro)  
        .circle(ri)  
        .extrude(extr_height)  
    )
    
    casing.export("motor_casing.stl")
    return casing  


#BATES CONFIGURATION

def bates_grain(outer_diam, inner_diam, grain_height):
    ro = (outer_diam/2)
    ri = (inner_diam/2)

    b_grain = (
        cq.Workplane('top')
        .circle(ro)
        .circle(ri)
        .extrude(grain_height)
    )
    b_grain.export("bates_grain.stl")
    
    return b_grain

def bulkhead_generic(hole_diam, outer_diam, t, h, a, b):
    rh = (hole_diam/2)
    ro = (outer_diam/2)

    bulk = (
        cq.Workplane('XY')
        .center(-rh,0)
        .moveTo(-rh,0)
        .lineTo(-ro,0)
        .lineTo(-ro,t)
        .lineTo(-ro+a,t)
        .lineTo(-ro+a,t+b)
        .lineTo(-ro,t+b)
        .lineTo(-ro,2*t+b)
        .lineTo(-ro+a,2*t+b)
        .lineTo(-ro+a,2*t+2*b)
        .lineTo(-ro,2*t+2*b)
        .lineTo(-ro,2*t+2*b+h)
        .lineTo(-rh,2*t+2*b+h)
        .lineTo(-rh,0)
        .close()
    )

    bulk_3d = (
        bulk.revolve(angleDegrees=360, axisStart=(0, 0, 0), axisEnd=(0, 1000, 0))
    )
    bulk_3d.export("bulkhead_generic.stl")

    return bulk_3d