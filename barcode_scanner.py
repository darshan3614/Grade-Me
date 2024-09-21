import cv2
from pyzbar.pyzbar import decode, ZBarSymbol

def decode_barcode(image):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray_img, symbols=[ZBarSymbol.CODE128, ZBarSymbol.QRCODE])  # Only decode CODE128 and QR codes

    for barcode in barcodes:
        x, y, w, h = barcode.rect
        barcode_info = barcode.data.decode('utf-8')
        cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(image, barcode_info, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        print("Decoded barcode data:", barcode_info)
        return barcode_info
    
    return None

# Capture video from the webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    barcode_info = decode_barcode(frame)
    if barcode_info:
        print(f"Detected barcode: {barcode_info}")
        # You can add code to send this information to your web server

    cv2.imshow('Barcode/QR code reader', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
