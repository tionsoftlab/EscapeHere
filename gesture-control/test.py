import cv2
import mediapipe as mp
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

last_detection_time = time.time()

prev_left_hand_pos = (0, 0)
prev_right_hand_pos = (0, 0)

horizontal_movement = False

left_circle_pos = (320, 120)
right_circle_pos = (320, 360)

while True:
    ret, frame = cap.read()
    
    if not ret:
        break
    
    frame = cv2.flip(frame, 1)
    
    height, width = frame.shape[:2]
    
    cv2.line(frame, (0, height // 2), (width, height // 2), (0, 255, 0), 2)
    cv2.line(frame, (width // 2, 0), (width // 2, height), (0, 255, 0), 2)
    
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)
    
    left_hand_pos = None
    right_hand_pos = None
    
    if results.multi_hand_landmarks and len(results.multi_hand_landmarks) == 2:
        landmarks = results.multi_hand_landmarks
        
        left_hand = landmarks[0] if landmarks[0].landmark[0].x < landmarks[1].landmark[0].x else landmarks[1]
        right_hand = landmarks[1] if landmarks[0].landmark[0].x < landmarks[1].landmark[0].x else landmarks[0]
        
        for id, lm in enumerate(left_hand.landmark):
            cx, cy = int(lm.x * width), int(lm.y * height)
            if id == 5:  # 왼손 중지 손가락 끝 좌표
                left_hand_pos = (cx, cy)
        
        for id, lm in enumerate(right_hand.landmark):
            cx, cy = int(lm.x * width), int(lm.y * height)
            if id == 17:  # 오른손 중지 손가락 끝 좌표
                right_hand_pos = (cx, cy)
        
        last_detection_time = time.time()
        
        if right_hand_pos[0] > prev_right_hand_pos[0]:
            horizontal_movement = True
        elif left_hand_pos[0] < prev_left_hand_pos[0]:
            horizontal_movement = True
        else:
            horizontal_movement = False
        
        if horizontal_movement:
            if left_hand_pos[1] > 0.4 * height and left_hand_pos[1] < 0.6 * height:
                left_circle_pos = (left_hand_pos[0], left_circle_pos[1])
            if right_hand_pos[1] > 0.4 * height and right_hand_pos[1] < 0.6 * height:
                right_circle_pos = (right_hand_pos[0], right_circle_pos[1])
        else:
            if left_hand_pos[0] > 0.4 * width and left_hand_pos[0] < 0.6 * width:
                left_circle_pos = (left_circle_pos[0], left_hand_pos[1])
            if right_hand_pos[0] > 0.4 * width and right_hand_pos[0] < 0.6 * width:
                right_circle_pos = (right_circle_pos[0], right_hand_pos[1])
        
        prev_left_hand_pos = left_hand_pos
        prev_right_hand_pos = right_hand_pos
    
    if time.time() - last_detection_time > 1:
        cv2.putText(frame, "양손을 드세요!", (width // 2 - 100, height // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    cv2.circle(frame, left_circle_pos, 10, (0, 0, 255), -1)
    
    cv2.circle(frame, right_circle_pos, 10, (255, 0, 0), -1)
    
    cv2.imshow('Camera', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
