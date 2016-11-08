void setup() {
    size(256,256);
    background(220);
    strokeWeight(3);
}

void draw() {
    if (mousePressed) {

	line(mouseX, mouseY, pmouseX, pmouseY);


    }
}

