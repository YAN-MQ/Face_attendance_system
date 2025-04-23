/**
 * 声音管理器 - 管理应用程序中的所有音效播放
 * 使用单例模式确保全局只有一个音频管理实例
 */
export class SoundManager {
  static instance = null;
  
  /**
   * 获取SoundManager的单例实例
   * @returns {SoundManager} 单例实例
   */
  static getInstance() {
    if (!SoundManager.instance) {
      SoundManager.instance = new SoundManager();
    }
    return SoundManager.instance;
  }
  
  constructor() {
    if (SoundManager.instance) {
      throw new Error('SoundManager是单例类，请使用SoundManager.getInstance()获取实例');
    }
    
    // 初始化音频对象
    this.sounds = {};
    this.volume = 0.5;
    this.muted = false;
    
    // 预加载常用音效
    this.preloadSounds();
  }
  
  /**
   * 预加载常用音效
   * @private
   */
  preloadSounds() {
    try {
      // 根据实际文件结构调整路径
      const soundFiles = {
        success: require('@/assets/sounds/success.mp3'),
        error: require('@/assets/sounds/error.mp3'),
        info: require('@/assets/sounds/info.mp3')
      };
      
      // 创建并预加载音频对象
      Object.entries(soundFiles).forEach(([key, src]) => {
        const audio = new Audio(src);
        audio.load();
        audio.volume = this.volume;
        this.sounds[key] = audio;
      });
      
      console.log('音效预加载完成');
    } catch (error) {
      console.error('预加载音效失败:', error);
    }
  }
  
  /**
   * 播放指定的音效
   * @param {string} type 音效类型 ('success'|'error'|'info')
   * @returns {Promise<void>}
   */
  async play(type) {
    if (this.muted || !this.sounds[type]) {
      return;
    }
    
    try {
      const sound = this.sounds[type];
      sound.currentTime = 0; // 重置音频位置
      await sound.play().catch(error => {
        console.warn(`播放${type}音效失败:`, error);
      });
    } catch (error) {
      console.error(`播放${type}音效失败:`, error);
    }
  }
  
  /**
   * 设置所有音效的音量
   * @param {number} value 音量值 (0.0-1.0)
   */
  setVolume(value) {
    this.volume = Math.max(0, Math.min(1, value));
    
    // 更新所有已加载的音效音量
    Object.values(this.sounds).forEach(audio => {
      audio.volume = this.volume;
    });
  }
  
  /**
   * 切换静音状态
   * @param {boolean} [value] 如果提供，则设置为指定值；否则切换当前状态
   * @returns {boolean} 切换后的静音状态
   */
  toggleMute(value = undefined) {
    if (value !== undefined) {
      this.muted = Boolean(value);
    } else {
      this.muted = !this.muted;
    }
    return this.muted;
  }
} 