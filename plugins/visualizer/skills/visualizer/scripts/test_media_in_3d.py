"""Behavioral checks for the optional media-in-3D audio adapter."""
import unittest
import numpy as np
from media_in_3d import audio_features, audio_onsets, audio_signals, MediaStudy


class AudioBindingTests(unittest.TestCase):
    def test_silence_has_no_motion(self):
        self.assertTrue(np.array_equal(audio_features(np.zeros(96000), 48000, 30, 60), np.zeros((60, 3))))

    def test_frequency_separation_and_leakage_floor(self):
        t = np.arange(96000) / 48000
        for frequency, expected in [(80, 0), (650, 1), (5000, 2)]:
            features = audio_features(.4 * np.sin(2 * np.pi * frequency * t), 48000, 30, 60)
            self.assertGreater(features[10:, expected].mean(), .9)
            for other in set(range(3)) - {expected}:
                self.assertLess(features[:, other].max(), .01)

    def test_short_or_nonfinite_audio_rejected(self):
        for pcm in [np.zeros(100), np.full(96000, np.nan)]:
            with self.assertRaises(ValueError):
                audio_features(pcm, 48000, 30, 60)

    def test_impulse_is_not_anticipated(self):
        pcm=np.zeros(96000); onset=24000
        t=np.arange(96000-onset)/48000
        pcm[onset:]=.4*np.sin(2*np.pi*80*t)
        features=audio_features(pcm,48000,30,60)
        self.assertEqual(features[:16].max(),0)  # Frame15 at.5s cannot see samples after.5s.
        self.assertGreater(features[16:20,0].max(),.7)
        self.assertEqual(audio_onsets(features)[:16].max(),0)
        self.assertGreater(audio_onsets(features)[16:19].max(),.5)

    def test_audio_changes_artwork_without_meters_or_camera_fit(self):
        from pathlib import Path
        font=Path('/System/Library/Fonts/Supplemental/Arial.ttf')
        if not font.is_file(): self.skipTest('Host rendering font unavailable')
        frames=np.full((2,768,432,3),[148,117,77],np.uint8)
        masks=np.zeros((2,768,432),np.uint8); masks[:,130:720,180:370]=255
        depth=np.full((768,432),.7)
        rest=MediaStudy(frames,np.zeros((450,3)),(720,1280),15,font,matte=masks,depth=depth)
        active=MediaStudy(frames,np.ones((450,3)),(720,1280),15,font,matte=masks,depth=depth)
        for frame in [150,360]:
            a=np.asarray(rest.render(frame))[205:1080,60:660].astype(float)
            b=np.asarray(active.render(frame))[205:1080,60:660].astype(float)
            self.assertGreater(np.mean(np.abs(a-b)),1)
        # The same fixed camera gives a larger geometric footprint when depth increases.
        pts=np.array([[-.5,1,.2],[.5,-1,.2]])
        far=rest.project(pts,.4); pts[:,2]+=.3; near=rest.project(pts,.4)
        self.assertGreater(np.ptp(near[:,1]),np.ptp(far[:,1]))

    def make_study(self, empty=False):
        from pathlib import Path
        font=Path('/System/Library/Fonts/Supplemental/Arial.ttf')
        if not font.is_file(): self.skipTest('Host rendering font unavailable')
        frames=np.full((120,768,432,3),[148,117,77],np.uint8)
        masks=np.zeros((120,768,432),np.uint8)
        if not empty: masks[:,130:720,180:370]=255
        return MediaStudy(frames,np.zeros((450,3)),(720,1280),15,font,matte=masks,depth=np.full((768,432),.7))

    def test_ground_is_aligned_to_visible_contact_not_padding(self):
        study=self.make_study()
        expected=1.4226-2.8452*719/767
        self.assertAlmostEqual(study.ground_y,expected,delta=.02)
        self.assertGreater(study.ground_y,-1.35)  # Canvas bottom would leave the subject floating.
        with self.assertRaisesRegex(ValueError,'no visible subject'):
            self.make_study(empty=True)

    def test_pose_contact_stays_on_floor_when_matte_bottom_moves(self):
        from PIL import Image
        study=self.make_study()
        study.masks[1]=np.roll(study.masks[1].reshape(228,128),-3,axis=0).ravel()
        captured=[]; project=study.project
        def observe(points,*args,**kwargs):
            captured.append(np.asarray(points).copy());return project(points,*args,**kwargs)
        study.project=observe
        study.cloud(Image.new('RGBA',(720,1280)),1,0,1,0,1,0,0,0,0,1)
        self.assertAlmostEqual(captured[0][:,1].min(),study.ground_y,delta=.015)

    def test_historical_poses_remain_stable_and_never_show_future(self):
        study=self.make_study()
        before=study.scene_state(250); after=study.scene_state(330)
        self.assertEqual([x[0] for x in before[3]][:6],[x[0] for x in after[3]][:6])
        for frame in range(240,340,5):
            lift,spread,index,layers=study.scene_state(frame)
            self.assertTrue(all(n<=index for n,_,_ in layers))
        # Staggered emergence: the oldest layer is visible before the nearest history starts.
        early=study.scene_state(252)[3]
        self.assertGreater(early[0][2],0)
        self.assertEqual(early[-1][2],0)

    def test_onset_from_raw_bands_is_causal_and_decays_after_step(self):
        pcm=np.zeros(96000); t=np.arange(72000)/48000
        pcm[24000:]=.4*np.sin(2*np.pi*80*t)
        bands,onsets=audio_signals(pcm,48000,30,60)
        np.testing.assert_allclose(bands,audio_features(pcm,48000,30,60))
        self.assertEqual(onsets[:16].max(),0)
        self.assertGreater(onsets[16:19].max(),.8)
        self.assertLess(onsets[30],.01)

    def test_bloom_respects_alpha_and_stays_local(self):
        from PIL import Image,ImageDraw
        study=self.make_study()
        base=Image.new('RGBA',(64,64),'black')
        results=[]
        for alpha in [255,128]:
            field=Image.new('RGBA',(64,64))
            ImageDraw.Draw(field).rectangle((27,27,36,36),fill=(180,130,70,alpha))
            results.append(np.asarray(study.composite_field(base.copy(),field,0,1)).astype(float))
        region=np.ones((64,64),bool);region[27:37,27:37]=False
        ratio=results[1][:,:,:3][region].sum()/results[0][:,:,:3][region].sum()
        self.assertGreater(ratio,.4);self.assertLess(ratio,.6)
        self.assertEqual(results[0][0,0,:3].max(),0)

    def test_stereo_fold_down_matches_mono(self):
        t = np.arange(96000) / 48000
        mono = .4 * np.sin(2 * np.pi * 80 * t)
        np.testing.assert_allclose(audio_features(np.column_stack([mono, mono]), 48000, 30, 60),
                                   audio_features(mono, 48000, 30, 60), atol=1e-12)


if __name__ == '__main__':
    unittest.main()
