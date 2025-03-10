# McDonald's Kafka Streaming Project

## Overview
This project implements a **real-time streaming data pipeline** using **Apache Kafka**, **MongoDB**, and **MongoDB Atlas**. The pipeline processes **McDonald's order and payment data**, joins the streams, and generates visual insights to analyze **trends in payment methods**.

## Architecture
The pipeline consists of the following components:

1. **Kafka Topics:**
   - `mcd_orders`: Stores mock order data.
   - `mcd_payments`: Stores mock payment data.

2. **Kafka Streams:**
   - `mcd_orders_stream`: Reads data from `mcd_orders`.
   - `mcd_payments_stream`: Reads data from `mcd_payments`.
   - `mcd_orders_payments_joined`: Joins the above two streams based on `order_id` and maintains a **persistent query**.

3. **MongoDB Sink:**
   - The joined data is stored in **MongoDB** for further processing.

4. **Visualization:**
   - Data is aggregated and visualized using **MongoDB Atlas** to analyze payment method trends via a **donut chart**.

## Data Flow
1. **Producers generate mock order and payment data** and send them to Kafka topics.
2. **Kafka Streams process the incoming data**, join the order and payment streams, and output the joined results.
3. **The joined stream is written to MongoDB** using the MongoDB sink connector.
4. **MongoDB Atlas aggregates the data** and visualizes payment trends.

## Technologies Used
- **Apache Kafka** (Topics, Producers, Streams)
- **Python** (Mock data generation, producer script)
- **MongoDB** (Storage and processing)
- **MongoDB Atlas** (Visualization)

## Getting Started
### Prerequisites
Ensure you have the following installed:
- Docker (for running Kafka & MongoDB locally)
- Python 3.8+
- Confluent Kafka Python library
- MongoDB & MongoDB Atlas account

### Setup
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/mcdonalds-kafka-streaming.git
   cd mcdonalds-kafka-streaming
   ```
2. **Start Kafka using Docker Compose:**
   ```bash
   docker-compose up -d
   ```
3. **Run the producer scripts to generate mock data:**
   ```bash
   python mcd_producer.py.py
   ```
4. **Start Kafka Streams processing:**
   
5. **Connect MongoDB Sink and visualize in MongoDB Atlas.**

## Visualization Example
- The donut chart in MongoDB Atlas aggregates the `payment_method` field and calculates the total payments for each method.

## Future Enhancements
- Add **alerting mechanisms** for unusual payment patterns.
- Extend the project to support **real-time fraud detection**.

## Contributing
Feel free to **fork the repository** and submit a PR with improvements!

## License
This project is licensed under the MIT License.
