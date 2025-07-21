import cv2
import cvzone
from cvzone.FaceMeshModule import FaceMeshDetector
import numpy as np

# Initialize face detector
detector = FaceMeshDetector(maxFaces=2)

# Load two face images
img1 = cv2.imread("face1.jpg")
img2 = cv2.imread("face2.jpg")

# Resize images (optional)
img1 = cv2.resize(img1, (640, 480))
img2 = cv2.resize(img2, (640, 480))

# Detect face landmarks
img1, faces1 = detector.findFaceMesh(img1)
img2, faces2 = detector.findFaceMesh(img2)

if faces1 and faces2:
    face1 = faces1[0]
    face2 = faces2[0]

    # Get convex hull indexes (to map the face)
    hull_indexes = detector.facemap['FACE']

    points1 = np.array([face1[i] for i in hull_indexes], dtype=np.int32)
    points2 = np.array([face2[i] for i in hull_indexes], dtype=np.int32)

    # Create Delaunay triangulation
    rect = cv2.boundingRect(points2)
    subdiv = cv2.Subdiv2D(rect)
    for p in points2:
        subdiv.insert((p[0], p[1]))
    triangles = subdiv.getTriangleList()
    triangles = np.array(triangles, dtype=np.int32)

    indexes_triangles = []
    for t in triangles:
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

        index1 = np.where((points2 == pt1).all(axis=1))[0]
        index2 = np.where((points2 == pt2).all(axis=1))[0]
        index3 = np.where((points2 == pt3).all(axis=1))[0]

        if index1.size and index2.size and index3.size:
            indexes_triangles.append([index1[0], index2[0], index3[0]])

    # Create a mask for face2
    mask = np.zeros_like(img2)
    for triangle in indexes_triangles:
        pts = np.array([points2[triangle[0]],
                        points2[triangle[1]],
                        points2[triangle[2]]], np.int32)
        cv2.fillConvexPoly(mask, pts, (255, 255, 255))

    # Warp face1 to face2
    img_face_swap = np.zeros_like(img2)
    for triangle in indexes_triangles:
        tri1 = np.array([points1[triangle[0]],
                         points1[triangle[1]],
                         points1[triangle[2]]], np.float32)
        tri2 = np.array([points2[triangle[0]],
                         points2[triangle[1]],
                         points2[triangle[2]]], np.float32)

        matrix = cv2.getAffineTransform(tri1, tri2)
        warped = cv2.warpAffine(img1, matrix, (img2.shape[1], img2.shape[0]))
        cv2.fillConvexPoly(img_face_swap, np.int32(tri2), (0, 0, 0))
        img_face_swap = cv2.add(img_face_swap, cv2.bitwise_and(warped, warped, mask=cv2.fillConvexPoly(np.zeros_like(mask[:,:,0]), np.int32(tri2), 255)))

    # Combine with original
    result = cv2.bitwise_and(img2, cv2.bitwise_not(mask))
    final = cv2.add(result, img_face_swap)

    # Show result
    cv2.imshow("Face Swapped", final)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

else:
    print("Face(s) not detected properly.")
