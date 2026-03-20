# Examples

## 10.1 Web端视频通话

```javascript
import TRTC from 'trtc-js-sdk';

const client = TRTC.createClient({
  sdkAppId: 1400000000,
  userId: 'user_' + Math.random(),
  userSig: '生成的UserSig',
  mode: 'videoCall'
});

async function startCall(roomId) {
  // 加入房间
  await client.join({ roomId });
  
  // 创建本地流
  const localStream = TRTC.createStream({
    userId: localUserId,
    audio: true,
    video: true
  });
  
  // 设置视频参数
  localStream.setVideoProfile('720p');
  
  // 初始化并发布
  await localStream.initialize();
  await client.publish(localStream);
  
  // 订阅远端流
  client.on('stream-added', async (event) => {
    const remoteStream = event.stream;
    await client.subscribe(remoteStream);
    remoteStream.play('remote-container');
  });
  
  // 离开房间
  document.getElementById('leave').onclick = async () => {
    await client.leave();
    localStream.close();
  };
}
```

## 10.2 Flutter多人视频会议

```dart
import 'package:tencent_trtc_cloud/tx_trtc_cloud.dart';
import 'package:tencent_trtc_cloud/tx_trtc_cloud_def.dart';

class TRTCService {
  late TXTRTCCloud trtcCloud;
  
  Future<void> joinRoom(int roomId, String userId) async {
    trtcCloud = TXTRTCCloud.sharedInstance();
    
    final params = TRTCParams(
      sdkAppId: 1400000000,
      userId: userId,
      userSig: _generateUserSig(userId),
      roomId: roomId,
      role: TRTCCloudDef.TRTCRoleAnchor
    );
    
    await trtcCloud.enterRoom(params);
    
    // 开启本地音频视频
    await trtcCloud.startLocalAudio(TRTCCloudDef.TRTCAudioQualityMusic);
    await trtcCloud.startLocalVideo();
  }
  
  // 渲染本地视频
  Widget buildLocalView() {
    return TXTRTCCloudVideoView(
      onViewCreated: (viewId) {
        trtcCloud.startLocalVideoPreview(viewId);
      }
    );
  }
}
```

## 10.3 实现屏幕分享

```javascript
// 屏幕分享
const screenStream = TRTC.createStream({
  userId: localUserId,
  audio: false,
  video: true,
  screenSet: {
    width: 1920,
    height: 1080,
    frameRate: 10
  }
});

await screenStream.initialize();
await client.publish(screenStream);

// 停止屏幕分享
await client.unpublish(screenStream);
screenStream.close();
```

## 10.4 混流(云端合流)

```dart
// 设置云端混流
final mixParams = TRTCTranscodingConfig(
  mode: TRTCCloudDef.TRTC_TranscodingConfig_Manual,
  videoWidth: 1920,
  videoHeight: 1080,
  videoBitrate: 1500,
  videoGOP: 2,
  audioBitrate: 64,
  audioSampleRate: 48000,
  mixUserList: [
    MixUser(
      userId: 'user1',
      roomId: 12345,
      zOrder: 1
    ),
    MixUser(
      userId: 'user2', 
      roomId: 12345,
      zOrder: 2
    )
  ]
);

await trtcCloud.setMixTranscodingConfig(mixParams);
```

## 10.5 通话质量监控

```javascript
// 监听通话质量
client.on('network-quality', (event) => {
  const { uplinkNetworkQuality, downlinkNetworkQuality } = event;
  
  // uplinkNetworkQuality: 上行网络质量 1-6 (1最好)
  // downlinkNetworkQuality: 下行网络质量 1-6 (1最好)
  
  if (uplinkNetworkQuality > 4) {
    console.warn('网络质量较差，建议降低画质');
  }
});

// 获取本地流统计信息
setInterval(() => {
  const stats = localStream.getStats();
  console.log(`FPS: ${stats.videoFrameRate}, 码率: ${stats.videoBitrate}`);
}, 2000);
```
