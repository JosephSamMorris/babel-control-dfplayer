import java.net.*;
import java.io.*;
import java.util.Arrays;

DatagramSocket socket;
DatagramPacket packet;

final int PORT = 4210;
final int UNIT_COUNT_IN_ARRAY = 178;
final int UNIT_COUNT_IN_PACKET = 180;
final int DATA_SIZE = 8;

final int ARRAY_COLUMNS = 13;
final int ARRAY_COLUMNS_SHORT = 11; // Short rows are missing 2 units
final int ARRAY_ROWS = 14;

byte[] rxBuffer = new byte[UNIT_COUNT_IN_PACKET * DATA_SIZE];

boolean timedOut = false;

void setup() {
  size(400, 600);
  smooth();
  
  try {
    socket = new DatagramSocket(4210);
    socket.setSoTimeout(1000);
  } catch (Exception e) {
    e.printStackTrace(); 
    println(e.getMessage());
  }
}

PVector positionFromIndex(int idx) {
  if (idx < ARRAY_COLUMNS * 6) {
    int y = idx / ARRAY_COLUMNS;
    int x = idx % ARRAY_COLUMNS;

    return new PVector(x, y);
  } else if (idx < ARRAY_COLUMNS * 6 + ARRAY_COLUMNS_SHORT * 2) {
    // We are going to start by ignoring the first 6 rows with 13 units each
    int adj_idx = idx - ARRAY_COLUMNS * 6;
    
    int y = adj_idx / ARRAY_COLUMNS_SHORT + 6;
    
    // The missing lights above the bar get notched out on the left
    int x = adj_idx % ARRAY_COLUMNS_SHORT + 2;
    
    return new PVector(x, y);
  } else {
    // We pretend that the middle 2 rows actually had 13 units instead of 11
    int adj_idx = idx + 2 * (ARRAY_COLUMNS - ARRAY_COLUMNS_SHORT);
    
    int y = adj_idx / ARRAY_COLUMNS;
    int x = adj_idx % ARRAY_COLUMNS;
    
    return new PVector(x, y); 
  }
}

void renderPacket(byte[] buffer) {
  if (buffer.length != (UNIT_COUNT_IN_PACKET * DATA_SIZE)) {
    // Ignore if incorrect length
    return;
  }
  
  float unitDrawSize = 20;
  float unitDrawSpacing = unitDrawSize * 1.5;

  // Center our rendering
  // There are 12 full columns and 2 short ones
  PVector arrayDrawDims = positionFromIndex(ARRAY_COLUMNS * 12 + ARRAY_COLUMNS_SHORT * 2 - 1);
  translate((width - arrayDrawDims.x * unitDrawSpacing) / 2, (height - arrayDrawDims.y * unitDrawSpacing) / 2);
  
  strokeWeight(1);
  ellipseMode(CENTER);
  int count = min(UNIT_COUNT_IN_PACKET, UNIT_COUNT_IN_ARRAY);

  for (int i = 0; i < count; i++) {
    int di = i * DATA_SIZE;
    
    int mode = buffer[di];

    if (mode != 0) {
      // Skip any packets that are not using the direct mode (0)
      continue;
    }

    float brightness = ((Byte.toUnsignedInt(buffer[di + 1]) << 8) | Byte.toUnsignedInt(buffer[di + 2])) / (float)0xffff;
    // In-between brightness and volume is the sound offset, which we do not need to render
    float volume = ((Byte.toUnsignedInt(buffer[di + 5]) << 8) | Byte.toUnsignedInt(buffer[di + 6])) / (float)0xffff;
    
    PVector pos = positionFromIndex(i);
    float x = pos.x * unitDrawSpacing;
    float y = pos.y * unitDrawSpacing;
    
    pushMatrix();
    
    translate(x, y);
    
    // Fill light band
    noStroke();
    fill(int(brightness * 255));
    ellipse(0, 0, unitDrawSize, unitDrawSize);
    
    // Fill the volume circle
    float speakerSize = unitDrawSize / 2;
    noStroke();
    fill(255, 100, 100);
    ellipse(0, 0, speakerSize, speakerSize);
    noStroke();
    fill(0, 0, 255);
    float volSize = map(volume, 0, 1, 0, speakerSize);
    ellipse(0, 0, volSize, volSize);
    
    // Draw outline
    
    stroke(0);
    noFill();
    ellipse(0, 0, unitDrawSize, unitDrawSize);
    
    popMatrix();
  }
}

void draw() {
  background(255);
  
  try {
    DatagramPacket packet = new DatagramPacket(rxBuffer, rxBuffer.length);
    socket.receive(packet);
    timedOut = false;
  } catch (SocketTimeoutException e) {
    timedOut = true;
  } catch (IOException e) {
    e.printStackTrace(); 
    println(e.getMessage());
  }
  
  if (timedOut) {
    background(0);
  } else {
    background(255);
  }
  
  renderPacket(rxBuffer);
}
