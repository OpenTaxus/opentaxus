/* badge programming dock
right now, only a few parameters for making a multi-dock
can be mounted with M.3 screws and bolts
USB held in place with M.2 set screw

todo: more parameters; upright orientation; badge origin at usb port; dock base at z=0; round corners
*/

xpitch=10;
ypitch=20;
zpitch=70;
rows=7;
cols=1;
//wall_thickness=2
//badgex=
//badgey=
//badgez=

module badge(){
    union(){
        //pcb edge track
        linear_extrude(68)
        polygon(points=[
        [0,0],
        [126,0],
        [126,100],
        [28,2],
        [0,2]
        ]);
        //battery cutout
        translate([0,-3,4])
            cube([126,23,60]);        
        //usb port
        translate([-80,0.5,34-5.5])
            cube([80,6.5,11]);
        //power switch
        translate([-2,0,45])
            cube([2,5,5]);
        //usb set screw
        screwhole([-6,15,34],[90,0,0],6.5,3);
        //mounting holes
//        screwholes();
        }
}

module badgearray(rows=1,cols=1){
  for (i=[0:rows-1])
    for (j=[0:cols-1])
      translate([-i*xpitch,i*ypitch,j*zpitch])
    badge();
}

module screwhole(origin,orientation,d1=7,d2=4){
  translate(origin)
    rotate(orientation){
      //larger hex inset hole for head/bolt
      cylinder(h=6, d=d1,center=true,$fn=6);
      //smaller hole for shaft
      cylinder(h=100, d=d2,center=true,$fn=12);
    }
}

module screwholes(){
    //bottom
    screwhole([0,10,14],[0,90,0]);
    screwhole([0,10,68-14],[0,90,0]);
    //left
    screwhole([25,10,4],[0,0,0]);
    screwhole([5,10,4],[0,0,0]);
    //right
    screwhole([25,10,64],[0,0,0]);
    screwhole([5,10,64],[0,0,0]);
}

module multibadgedock(rows=1,cols=1){
  difference(){
    union(){
      translate([0,-2,-2])
        linear_extrude(zpitch*cols+2)
          polygon(points=[
            [45,0],
            [-rows*xpitch,0],
            [-rows*xpitch,ypitch*rows-1],
            [45-rows*xpitch,ypitch*rows-1]
          ]);
    }
    //carve out the badges
    badgearray(rows,cols);
    //clip the pointy top
    translate([43,-2,-2])cube([10,10,zpitch*cols+4]);
  }
}

single=true;
single=false;
dock=true;
//dock=false;

if (single){rows=1;cols=1;}
if (dock){
    multibadgedock(rows,cols);
}else{
    badgearray(rows,cols);
}