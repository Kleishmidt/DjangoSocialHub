const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
module.exports = {
    entry: './src/js/index.js',
    mode: 'development',
    output: {
        filename: 'index.js',
        path: path.resolve(__dirname, 'blog/static/blog/js'),
    },
    module: {
        rules: [
            {
                test: /\.(scss)$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader',
                    'sass-loader'
                ]
            },
        ]
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: '../css/index.css'
        })
    ]
};