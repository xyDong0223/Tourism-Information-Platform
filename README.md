# TeamNotFound

## Description
This is a group project for COMP30220 Distributed Systems.

Link to the video showcasing the project: https://youtu.be/dEv5yp5S_SU


### Built With

* Python
* Flask

### Port Usage

| Service           | Port Number |
|-------------------|-------------|
| client            | 5000        |
| serviceKiwi       | 5001        |
| serviceTrip       | 5002        |
| serviceSkyscanner | 5003        |
| serviceBooking    | 5004        |
| broker            | 5005        |

## Getting Started

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.

```sh
pip install -r requirements.txt
```

### Run in Local

* Start service 1 Booking
     ```sh
    cd serviceBooking 
    ```
    ```sh
    flask run --port=5004
    ```
* Start service 2 Kiwi
     ```sh
    cd serviceKiwi 
    ```
    ```sh
    flask run --port=5001
    ```
* Start service 3 Skyscanner
     ```sh
    cd serviceSkyscanner 
    ```
    ```sh
    flask run --port=5003
    ```
* Start service 4 Trip
      ```sh
    cd serviceTrip
    ```
    ```sh
    flask run --port=5002
    ```
* Start broker
    ```sh
    python broker/app.py
    ```
* Start client
    ```sh
    python app.py
    ```
Visit http://127.0.0.1:5000 for the website.

## Containerisation

* Run the docker compose up
    ```sh
    docker compose up
    ```

There are 6 containern running
1. service-booking
2. service-kiwi
3. service-trip
4. service-skyscanner
5. broker
6. client

Visit http://127.0.0.1:5000 for the website.



## Contact

Nan Wu - [@stevennanw](https://gitlab.com/stevennanw) - nan.wu1@ucdconnect.ie

Yiming Zhao - [@YimingZhao6324](https://gitlab.com/YimingZhao6324) - yiming.zhao2@ucdconnect.ie


Weijiong You - [@JoeYou](https://gitlab.com/JoeYou) - weijiong.you@ucdconnect.ie

Xinyu Dong - [@xyDong0223](https://gitlab.com/xyDong0223) - xinyu.dong@ucdconnect.ie

