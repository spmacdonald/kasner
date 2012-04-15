
void setup() {
  size(500, 500);
  noLoop();
}

void draw() {

  float s = 100;
  float x0 = 2;
  float y0 = 0;

  float x1 = -1;
  float y1 = sqrt(3);

  float x2 = -1;
  float y2 = -sqrt(3);

  translate(width/2, height/2);

  ellipse(0, 0, 2*s, 2*s);
  line(s*x0, s*y0, s*x1, s*y1);
  line(s*x0, s*y0, s*x2, s*y2);
  line(s*x1, s*y1, s*x2, s*y2);

  // Angle algorithm tests.
  // float th = 0.27092;
  // ellipse(s*cos(th), s*sin(th),10,10);

  // th = nextAngle(th);
  // ellipse(s*cos(th), s*sin(th),10,10);

  // th = nextAngle(th - 2*PI/3) + 2*PI/3;
  // ellipse(s*cos(th), s*sin(th),10,10);

  // th = nextAngle(th - 4*PI/3) + 4*PI/3;
  // ellipse(s*cos(th), s*sin(th),10,10);

  // println(th);

  // line(s*cos(th1), s*sin(th1), s*cos(th2), s*sin(th2));

  float th = -0.2;
  line(s*cos(th), s*sin(th), s*-1, s*sqrt(3));
  line(s*cos(th), s*sin(th), s*-1, -s*sqrt(3));
  line(s*cos(th), s*sin(th), s*2, 0);
  ellipse(s*cos(th), s*sin(th),10,10);

  th = lastAngle(th, 2);
  fill(15);
  ellipse(s*cos(th), s*sin(th),10,10);

}

float lastAngle(float th, int i) {

  // Rotate th to -pi/3 < th < pi/3
  float x = 0;
  if (th >= PI/3 && th < PI) {
    x = 2*PI/3;
    th -= x;

    if (i == 0) {
      return acos( (5*cos(th + 2*PI/3) - 4)/(4*cos(th + 2*PI/3) - 5) ) - 2*PI/3 + x;
    }
    else if (i == 1) {
      return -acos( (5*cos(th + 4*PI/3) - 4)/(4*cos(th + 4*PI/3) - 5) ) - 4*PI/3 + x;
    }
    else {
      return th + x;
    }
  }
  else if (th >= PI && th < 5*PI/3) {
    x = 4*PI/3;
    th -= x;

    if (i == 0) {
      return -acos( (5*cos(th + 4*PI/3) - 4)/(4*cos(th + 4*PI/3) - 5) ) - 4*PI/3 + x;
    }
    else if (i == 2) {
      return acos( (5*cos(th + 2*PI/3) - 4)/(4*cos(th + 2*PI/3) - 5) ) - 2*PI/3 + x;
    }
    else {
      return th + x;
    }
  }
  else {
    if (i == 1) {
      return acos( (5*cos(th + 2*PI/3) - 4)/(4*cos(th + 2*PI/3) - 5) ) - 2*PI/3;
    }
    else if (i == 2) {
      return -acos( (5*cos(th + 4*PI/3) - 4)/(4*cos(th + 4*PI/3) - 5) ) - 4*PI/3;
    }
    else {
      return th;
    }
  }
}

float nextAngle(float th) {
  return -acos( (5*cos(th) - 4)/(4*cos(th) - 5) );
}
