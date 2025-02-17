module.exports = {
  "presets": [
    "@babel/preset-env"
  ]
}
chainWebpack: (config) => {
  config
      .plugin('html')
      .tap(args => {
          args[0].title = 'MyApp title';
          args[0].meta = {viewport: 'content="width=device-width, initial-scale=1.0'};

       return args;
  })
}
