#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# This file is a part of servocam.org package <servocam.org>
# Created By: Marcin Szczygliński <info@servocam.org>
# GitHub: https://github.com/servo-cam
# License: MIT
# Updated At: 2023.03.27 02:00
# =============================================================================

movenet = {
    # model config
    'detector': {
        'movenet_single_pose_thunder_4': {
            'net': 'movenet',
            'dims': [256, 256],
        },
        'movenet_single_pose_lightning_4': {
            'net': 'movenet',
            'dims': [192, 192],
        },
        'movenet_multi_pose_lightning_1': {
            'net': 'movenet',
            'dims': [256, 256],
        }
    },
    # joints idx
    'idx': {
        'nose': 0,
        'left_eye': 1,
        'right_eye': 2,
        'left_ear': 3,
        'right_ear': 4,
        'left_shoulder': 5,
        'right_shoulder': 6,
        'left_elbow': 7,
        'right_elbow': 8,
        'left_wrist': 9,
        'right_wrist': 10,
        'left_hip': 11,
        'right_hip': 12,
        'left_knee': 13,
        'right_knee': 14,
        'left_ankle': 15,
        'right_ankle': 16
    },
    # paths between points
    'paths': {
        # left hip > left knee
        'l_hip_l_knee': {
            'fx': ['left_hip'],
            'fy': ['left_hip'],
            'tx': ['left_knee'],
            'ty': ['left_knee'],
            'score': ['left_knee'],
            'rgb': [42, 163, 69]
        },
        # right hip > right knee
        'r_hip_r_knee': {
            'fx': ['right_hip'],
            'fy': ['right_hip'],
            'tx': ['right_knee'],
            'ty': ['right_knee'],
            'score': ['right_knee'],
            'rgb': [42, 163, 69]
        },
        # hips (mid-point)
        'hip_l_m': {  # left
            'fx': ['left_hip'],
            'fy': ['left_hip'],
            'tx': ['left_hip', 'right_hip'],
            'ty': ['left_hip', 'right_hip'],
            'score': ['left_hip', 'right_hip'],
            'rgb': [140, 232, 90]
        },
        'hip_r_m': {  # right
            'fx': ['right_hip'],
            'fy': ['right_hip'],
            'tx': ['left_hip', 'right_hip'],
            'ty': ['left_hip', 'right_hip'],
            'score': ['left_hip', 'right_hip'],
            'rgb': [140, 232, 90]
        },
        # hip to shoulders
        'hip_l_shoulder_l': {  # left
            'fx': ['left_hip'],
            'fy': ['left_hip'],
            'tx': ['left_shoulder'],
            'ty': ['left_shoulder'],
            'score': ['left_hip', 'left_shoulder'],
            'rgb': [242, 85, 240]
        },
        'hip_r_shoulder_r': {  # right
            'fx': ['right_hip'],
            'fy': ['right_hip'],
            'tx': ['right_shoulder'],
            'ty': ['right_shoulder'],
            'score': ['right_hip', 'right_shoulder'],
            'rgb': [242, 85, 240]
        },
        # left knee > left ankle
        'l_knee_l_ankle': {
            'fx': ['left_knee'],
            'fy': ['left_knee'],
            'tx': ['left_ankle'],
            'ty': ['left_ankle'],
            'score': ['left_ankle'],
            'rgb': [140, 232, 90]
        },
        # right knee > right ankle
        'r_knee_r_ankle': {
            'fx': ['right_knee'],
            'fy': ['right_knee'],
            'tx': ['right_ankle'],
            'ty': ['right_ankle'],
            'score': ['right_ankle'],
            'rgb': [140, 232, 90]
        },
        # hips > shoulders
        'hips_shoulders_m': {
            'fx': ['left_hip', 'right_hip'],
            'fy': ['left_hip', 'right_hip'],
            'tx': ['left_shoulder', 'right_shoulder'],
            'ty': ['left_shoulder', 'right_shoulder'],
            'score': ['left_hip', 'right_hip'],
            'rgb': [242, 85, 240]
        },
        # shoulders (mid-point)
        'shoulder_l_m': {  # left
            'fx': ['left_shoulder'],
            'fy': ['left_shoulder'],
            'tx': ['left_shoulder', 'right_shoulder'],
            'ty': ['left_shoulder', 'right_shoulder'],
            'score': ['left_shoulder', 'right_shoulder'],
            'rgb': [92, 70, 235]
        },
        'shoulder_r_m': {  # right
            'fx': ['right_shoulder'],
            'fy': ['right_shoulder'],
            'tx': ['left_shoulder', 'right_shoulder'],
            'ty': ['left_shoulder', 'right_shoulder'],
            'score': ['left_shoulder', 'right_shoulder'],
            'rgb': [92, 70, 235]
        },
        # shoulders (mid-point) > nose (neck)
        'neck': {
            'fx': ['left_shoulder', 'right_shoulder'],
            'fy': ['left_shoulder', 'right_shoulder'],
            'tx': ['left_ear', 'right_ear'],
            'ty': ['left_ear', 'right_ear'],
            'score': ['left_shoulder', 'right_shoulder'],
            'rgb': [92, 108, 145]
        },
        # left shoulder > left elbow
        'l_shoulder_l_elbow': {
            'fx': ['left_shoulder'],
            'fy': ['left_shoulder'],
            'tx': ['left_elbow'],
            'ty': ['left_elbow'],
            'score': ['left_elbow'],
            'rgb': [245, 129, 66]
        },
        # right shoulder > right elbow
        'r_shoulder_r_elbow': {
            'fx': ['right_shoulder'],
            'fy': ['right_shoulder'],
            'tx': ['right_elbow'],
            'ty': ['right_elbow'],
            'score': ['right_elbow'],
            'rgb': [245, 129, 66]
        },
        # left elbow > left wrist
        'l_elbow_l_wrist': {
            'fx': ['left_elbow'],
            'fy': ['left_elbow'],
            'tx': ['left_wrist'],
            'ty': ['left_wrist'],
            'score': ['left_wrist'],
            'rgb': [227, 156, 118]
        },
        # right elbow > right wrist
        'r_elbow_r_wrist': {
            'fx': ['right_elbow'],
            'fy': ['right_elbow'],
            'tx': ['right_wrist'],
            'ty': ['right_wrist'],
            'score': ['right_wrist'],
            'rgb': [227, 156, 118]
        },
        # nose > left eye
        'nose_l_eye': {
            'fx': ['nose'],
            'fy': ['nose'],
            'tx': ['left_eye'],
            'ty': ['left_eye'],
            'score': ['left_eye'],
            'rgb': [255, 0, 0]
        },
        # nose > right eye
        'nose_r_eye': {
            'fx': ['nose'],
            'fy': ['nose'],
            'tx': ['right_eye'],
            'ty': ['right_eye'],
            'score': ['right_eye'],
            'rgb': [255, 0, 0]
        },
        # left eye > left ear
        'l_eye_l_ear': {
            'fx': ['left_eye'],
            'fy': ['left_eye'],
            'tx': ['left_ear'],
            'ty': ['left_ear'],
            'score': ['left_ear'],
            'rgb': [197, 217, 15]
        },
        # right eye > right ear
        'r_eye_r_ear': {
            'fx': ['right_eye'],
            'fy': ['right_eye'],
            'tx': ['right_ear'],
            'ty': ['right_ear'],
            'score': ['right_eye'],
            'rgb': [197, 217, 15]
        }
    }
}
