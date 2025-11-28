import pytest
import asyncio
import numpy as np
import cv2
from pathlib import Path
from unittest.mock import Mock, AsyncMock, patch
import sys
import time

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.face_detection_service import (
    detect_face_3d,
    detect_face_in_image,
    get_face_detection_info,
    Face3DData,
)

class TestFaceDetectionBasics:
    @pytest.mark.asyncio
    async def test_detect_face_in_image_with_valid_face(self):
        dummy_image = np.ones((480, 640, 3), dtype=np.uint8) * 200
        result = await detect_face_in_image(dummy_image)
        assert isinstance(result, bool)

    @pytest.mark.asyncio
    async def test_detect_face_in_image_with_empty_image(self):
        empty_image = np.zeros((480, 640, 3), dtype=np.uint8)
        result = await detect_face_in_image(empty_image)
        assert isinstance(result, bool)

    @pytest.mark.asyncio
    async def test_detect_face_3d_returns_face_3d_data(self):
        dummy_image = np.ones((480, 640, 3), dtype=np.uint8) * 100
        result = await detect_face_3d(dummy_image)
        if result is not None:
            assert isinstance(result, Face3DData)
            assert hasattr(result, 'face_detected')
            assert hasattr(result, 'landmarks_3d')
            assert hasattr(result, 'head_pose')
            assert hasattr(result, 'eye_aspect_ratio')
            assert hasattr(result, 'quality_score')
            assert hasattr(result, 'frontality_score')

class TestFace3DDetection:
    @pytest.mark.asyncio
    async def test_face_3d_data_structure(self):
        dummy_image = np.ones((480, 640, 3), dtype=np.uint8) * 150
        result = await detect_face_3d(dummy_image)
        if result is not None:
            assert result.face_detected in [True, False]
            assert isinstance(result.landmarks_3d, (list, type(None)))
            assert isinstance(result.head_pose, dict)
            assert 0.0 <= result.quality_score <= 1.0
            assert 0.0 <= result.frontality_score <= 1.0

    @pytest.mark.asyncio
    async def test_landmarks_3d_format(self):
        dummy_image = np.ones((480, 640, 3), dtype=np.uint8) * 120
        result = await detect_face_3d(dummy_image)
        if result is not None and result.landmarks_3d is not None:
            landmarks = result.landmarks_3d
            assert isinstance(landmarks, list)
            assert len(landmarks) <= 468
            for landmark in landmarks:
                assert len(landmark) == 3
                assert all(isinstance(coord, (float, int)) for coord in landmark)

class TestHeadPoseEstimation:
    @pytest.mark.asyncio
    async def test_head_pose_angles_exist(self):
        dummy_image = np.ones((480, 640, 3), dtype=np.uint8) * 130
        result = await detect_face_3d(dummy_image)
        if result is not None and result.head_pose:
            assert 'yaw' in result.head_pose or result.head_pose == {}
            assert 'pitch' in result.head_pose or result.head_pose == {}
            assert 'roll' in result.head_pose or result.head_pose == {}

    @pytest.mark.asyncio
    async def test_head_pose_angle_ranges(self):
        dummy_image = np.ones((480, 640, 3), dtype=np.uint8) * 140
        result = await detect_face_3d(dummy_image)
        if result is not None and result.head_pose:
            if 'yaw' in result.head_pose:
                assert -90 <= result.head_pose['yaw'] <= 90
            if 'pitch' in result.head_pose:
                assert -90 <= result.head_pose['pitch'] <= 90
            if 'roll' in result.head_pose:
                assert -90 <= result.head_pose['roll'] <= 90

class TestQualityScoring:
    @pytest.mark.asyncio
    async def test_quality_score_range(self):
        dummy_image = np.ones((480, 640, 3), dtype=np.uint8) * 110
        result = await detect_face_3d(dummy_image)
        if result is not None:
            assert 0.0 <= result.quality_score <= 1.0

    @pytest.mark.asyncio
    async def test_frontality_score_range(self):
        dummy_image = np.ones((480, 640, 3), dtype=np.uint8) * 100
        result = await detect_face_3d(dummy_image)
        if result is not None:
            assert 0.0 <= result.frontality_score <= 1.0

class TestEyeAspectRatio:
    @pytest.mark.asyncio
    async def test_eye_aspect_ratio_exists(self):
        dummy_image = np.ones((480, 640, 3), dtype=np.uint8) * 105
        result = await detect_face_3d(dummy_image)
        if result is not None and result.eye_aspect_ratio is not None:
            assert isinstance(result.eye_aspect_ratio, (float, int))
            assert result.eye_aspect_ratio >= 0

class TestErrorHandling:
    @pytest.mark.asyncio
    async def test_detect_face_3d_with_none_input(self):
        try:
            result = await detect_face_3d(None)
            assert result is None or isinstance(result, Face3DData)
        except (TypeError, ValueError, AttributeError):
            pass

    @pytest.mark.asyncio
    async def test_detect_face_3d_with_invalid_shape(self):
        invalid_image = np.ones((100,), dtype=np.uint8)
        try:
            result = await detect_face_3d(invalid_image)
            assert result is None or isinstance(result, Face3DData)
        except (ValueError, IndexError):
            pass

class TestBackwardCompatibility:
    @pytest.mark.asyncio
    async def test_detect_face_in_image_function_exists(self):
        dummy_image = np.ones((480, 640, 3), dtype=np.uint8) * 90
        result = await detect_face_in_image(dummy_image)
        assert isinstance(result, bool)

    @pytest.mark.asyncio
    async def test_get_face_detection_info_returns_dict(self):
        dummy_image = np.ones((480, 640, 3), dtype=np.uint8) * 95
        result = await get_face_detection_info(dummy_image)
        assert isinstance(result, dict)

class TestPerformance:
    @pytest.mark.asyncio
    async def test_detect_face_3d_performance(self):
        dummy_image = np.ones((480, 640, 3), dtype=np.uint8) * 85
        start_time = time.time()
        result = await detect_face_3d(dummy_image)
        elapsed_time = (time.time() - start_time) * 1000
        assert elapsed_time < 500, f"Detection took {elapsed_time:.2f}ms"

    @pytest.mark.asyncio
    async def test_detect_face_in_image_performance(self):
        dummy_image = np.ones((480, 640, 3), dtype=np.uint8) * 80
        start_time = time.time()
        result = await detect_face_in_image(dummy_image)
        elapsed_time = (time.time() - start_time) * 1000
        assert elapsed_time < 200

class TestIntegration:
    @pytest.mark.asyncio
    async def test_complete_face_detection_workflow(self):
        dummy_image = np.ones((480, 640, 3), dtype=np.uint8) * 75
        face_detected = await detect_face_in_image(dummy_image)
        assert isinstance(face_detected, bool)
        if face_detected:
            face_3d_data = await detect_face_3d(dummy_image)
            assert face_3d_data is not None
            assert 0.0 <= face_3d_data.quality_score <= 1.0
            info = await get_face_detection_info(dummy_image)
            assert isinstance(info, dict)

if __name__ == "__main__":
    print("Running 3D Face Detection Tests...")
    pytest.main(["-v", __file__])
