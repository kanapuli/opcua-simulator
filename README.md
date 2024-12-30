# Dairy Enterprise OPC UA Simulator

A comprehensive OPC UA server simulation of a dairy enterprise with multiple production lines, storage facilities, and quality control systems.

## Overview

This simulator creates an OPC UA server that models a dairy enterprise with the following components:
- Multiple production lines (Milk, Cheese, Yogurt, Ice Cream)
- Storage facilities (Milk Storage Tank, Cold Storage)
- Quality Control System
- Equipment monitoring and control

## OPC UA Node Structure

### Enterprise Node
The root node representing the dairy enterprise.

```
Enterprise (Object)
├── TotalMilkProcessed (Variable, Double) [Example: 1234.5]
├── ProductionStatus (Variable, Boolean) [Example: true]
├── Methods
│ ├── StartProduction()
│ └── StopProduction()
├── Storage (Object)
│ ├── MilkStorageTank
│ └── ColdStorage
├── QualityControl (Object)
└── ProductionLines (Object)
    ├── MilkProcessingLine
    ├── CheeseProductionLine
    ├── YogurtProductionLine
    └── IcecreamProductionLine
```

### Production Line Node Structure
Each production line contains:

```
ProductionLine (Object)
├── ProductionRate (Variable, Double) [Example: 0.7]
├── Efficiency (Variable, Double) [Example: 0.85]
└── BatchId (Property, String) [Example: "batch-12"]
```

## Components

### Enterprise Class
The Enterprise class is the root component that manages the entire factory:

- **Variables**:
  - TotalMilkProcessed (Double)
  - ProductionStatus (Boolean)
- **Methods**:
  - StartProduction()
  - StopProduction()
- **Components**:
  - Storage Management
  - Quality Control System
  - Multiple Production Lines

### Production Line Class
Each production line is managed by the ProductionLine class:

- **Variables**:
  - ProductionRate (Double): Current production rate (0.0 - 1.0)
  - Efficiency (Double): Production line efficiency (0.0 - 1.0)
  - BatchId (String): Current batch identifier
- **Features**:
  - Real-time simulation of production metrics
  - Equipment management
  - Batch processing capabilities


### Equipment Class
The Equipment class represents individual machines in the production line:

- **Configurable Components**:
  - Variables (with random value simulation)
  - Properties
  - Methods
- **Supported Data Types**:
  - Float: Temperature readings
  - Double: Pressure readings
  - Boolean: Status indicators
  - String: State descriptions
  - Int32/Int64/Int16: Counter values

## Running the Application

### Using Docker

1. Build the image:
```
docker build -t dairy-enterprise .
```

2. Run the container:
```
docker run -p 4840:4840 dairy-enterprise
```

### Local Development

```
python -m venv venv
source venv/bin/activate # Linux/Mac
.\venv\Scripts\activate # Windows
```

1. Install dependencies:
```
pip install -r requirements.txt
```

2. Run the application:
```
python main.py
```

3. Access the OPC UA server:
```
http://localhost:4840/opcua/
```

## OPC UA Server Details

- **Endpoint**: opc.tcp://0.0.0.0:4840/freeopcua/server
- **Namespace**: https://kanapuli.github.io/dairy-enterprise

## Simulation Features

- Real-time variable updates (1-2 second intervals)
- Random value generation within realistic ranges
- Concurrent simulation of multiple production lines
- Equipment variable monitoring
- Production status tracking
- Batch processing simulation

## Data Types and Examples

| Node Type | Data Type | Example Value | Update Frequency |
|-----------|-----------|---------------|------------------|
| ProductionRate | Double | 0.7 | 1 second |
| Efficiency | Double | 0.85 | 1 second |
| BatchId | String | "batch-12" | On batch change |
| Temperature | Float | 72.5 | 2 seconds |
| Status | Boolean | true | 2 seconds |
| Counter | Int32 | 75 | 2 seconds |