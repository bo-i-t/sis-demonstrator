module.exports = {
  publicPath: process.env.NODE_ENV === 'production'
  ? '/production-sub-path/'
  :'/humaine',
  devServer: {
    proxy: {
      'https://bo-i-t.selfhost.eu/humaine': {
        target: 'http://192.168.102.59:8080'
        },
      '/humaine': {
        target: 'http://backend:8000',
        secure: false,
        changeOrigin: true,
      }
    }
  }
}