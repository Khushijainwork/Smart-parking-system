# Smart-parking-system
This project aims to develop a full-stack IoT application that provides a smart parking system. The application allows the user to book a parking slot in advance using a web-based application developed using HTML and CSS. Once the booking is confirmed, a servo motor raises a barrier, allowing the user to park the vehicle. An ultrasound detector is installed at the parking slot, which senses the arrival of the car and sends a signal to the application. Upon leaving the parking slot, the barrier is lowered automatically, and the parking space becomes available for other users to book.
Users can create an account in the web application and use a GUI to book a parking bay.
The application provides real-time information about parking availability, and the user can also use the app to lower the barrier and exit the parking slot. Overall, this project aims to provide a convenient and efficient parking solution that utilizes IoT technology to simplify the parking process for the user.
#Requires
flask
flask-socketio
pyserial
