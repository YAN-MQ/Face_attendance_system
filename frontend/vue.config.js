module.exports = {
  transpileDependencies: ['vuetify'],
  // 简化配置，避免访问未定义的plugins
  configureWebpack: {
    module: {
      rules: [
        {
          test: /\.js$/,
          exclude: /node_modules/,
          use: {
            loader: 'babel-loader'
          }
        }
      ]
    }
  }
}
