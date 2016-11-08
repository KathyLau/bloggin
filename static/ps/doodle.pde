float edgelength;
float drawColor;
float drawSize;

void setup() {
    size(256,256);
    background(255);
    fill(235);
    stroke(235);
    ellipse(width/2, height/2, width, width);
    edgelength = (dist(0,0,width/2, width/2) - (128 * sin(radians(45)) * sqrt(2))) / sqrt(2);
    strokeWeight(5);
    fill(0);
    stroke(0);
    textAlign(CENTER, CENTER);
    drawColor = 0;
    drawSize = 5;
}

void draw() {
    // Clear Button
    if (mouseX <= edgelength && mouseY <= edgelength) {
	strokeWeight(1);
	stroke(200);
	fill(200);
	rect(0,0, edgelength, edgelength);
	stroke(0);
	fill(0);
	text("Clear", edgelength/2, edgelength/2);
    } else if (mouseX >= width-edgelength && mouseX <= width && mouseY <= edgelength) {
	strokeWeight(1);
	stroke(200);
	fill(200);
	rect(width-edgelength,0, edgelength, edgelength);
	stroke(0);
	fill(0);
	if (drawColor == 0) {
	    text("Erase", width-edgelength/2, edgelength/2);
	} else {
	    text("Draw", width-edgelength/2, edgelength/2);
	}
    } else if (mouseX <= edgelength && mouseY >= height - edgelength && mouseY <= height) {
	strokeWeight(1);
	stroke(200);
	fill(200);
	rect(0,height-edgelength, edgelength, edgelength);
	stroke(0);
	fill(0);
	text("-", edgelength/2, height - edgelength/2);
    } else if (mouseX >= width-edgelength && mouseX <= width && mouseY >= height-edgelength && mouseY <= height) {
	strokeWeight(1);
	stroke(200);
	fill(200);
	rect(width-edgelength,height-edgelength, edgelength, edgelength);
	stroke(0);
	fill(0);
	text("+", width - edgelength/2, height - edgelength/2);
    } else {
	strokeWeight(1);
	stroke(255);
	fill(255);
	rect(0,0,edgelength, edgelength);
	rect(width-edgelength,0, edgelength, edgelength);
	rect(0,height-edgelength, edgelength, edgelength);
	rect(width-edgelength,height-edgelength, edgelength, edgelength);
	strokeWeight(drawSize);
	stroke(drawColor);
    }
    smooth();
    if (mousePressed && dist(pmouseX, pmouseY, width/2, height/2)<128 && dist(mouseX, mouseY, width/2, height/2)<128) {
	line(mouseX, mouseY, pmouseX, pmouseY);
    }
}

void mousePressed(){
    if (mouseX <= edgelength && mouseY <= edgelength) {
	fill(235);
	stroke(235);
	ellipse(width/2, height/2, width, width);
    } else if (mouseX >= width-edgelength && mouseX <= width && mouseY <= edgelength) {
	drawColor = abs(drawColor - 235);
    } else if (mouseX <= edgelength && mouseY >= height - edgelength && mouseY <= height) {
	drawSize-=3;
    } else if (mouseX >= width-edgelength && mouseX <= width && mouseY >= height-edgelength && mouseY <= height) {
	drawSize+=3;
    }
}
