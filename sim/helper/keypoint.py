import numpy as np

# MediaPipe landmark indices used by LEAP retargeter
WRIST, THUMB_TIP, INDEX_TIP, MIDDLE_TIP, RING_TIP = 0, 4, 8, 12, 16

def make_keypoints(open_amount: float = 1.0) -> np.ndarray:
    """
    open_amount in [0, 1]: 1.0 = fully open, 0.0 = full fist.
    Builds a 21x3 array; only indices 0, 4, 8, 12, 16 matter for vector retargeting.
    Frame: +X palm-normal (out of palm), +Y wrist->fingertip, +Z thumb-side.
    Units: metres. Retargeter scales internally with scaling_factor=1.6.
    """
    kp = np.zeros((21, 3), dtype=np.float32)

    L_finger = 0.09     # wrist->fingertip length when open (~9 cm)
    L_thumb  = 0.07     # wrist->thumbtip length when open
    a = open_amount     # 1.0 open, 0.0 fist

    # Open hand: tips lie along +Y, well in front of wrist.
    # Fist:      tips lie close to palm (small +Y) and curled toward palm (+X reduced, slight -X).
    def tip(side_z, length, thumb=False):
        # side_z places fingers along Z axis (negative for pinky side, positive for thumb side)
        # interpolate between open (mostly +Y) and fist (close to wrist, slight -X)
        y_open  = length
        y_fist  = 0.02
        x_open  = 0.0
        x_fist  = -0.03 if not thumb else -0.015
        x = x_open * a + x_fist * (1 - a)
        y = y_open * a + y_fist * (1 - a)
        return np.array([x, y, side_z], dtype=np.float32)

    kp[WRIST]      = [0.0, 0.0,  0.0]
    kp[THUMB_TIP]  = tip(side_z= 0.040, length=L_thumb, thumb=True)
    kp[INDEX_TIP]  = tip(side_z= 0.020, length=L_finger)
    kp[MIDDLE_TIP] = tip(side_z= 0.000, length=L_finger)
    kp[RING_TIP]   = tip(side_z=-0.020, length=L_finger)
    return kp