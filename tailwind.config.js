
module.exports = {
    content: [
        './**/*.{html,js}',
    ],
    theme: {
        extend: {
            width: {
                'khg-quarter': '10rem',
                'khg-half': '20rem',
                'khg-quarter3': '30rem',
                'khg-full': '40rem',
            },
            height: {
                'khg-quarter': '10rem',
                'khg-half': '20rem',
                'khg-full': '40rem',
            },
            minWidth: {
                'khg-half': '20rem',
            },
            maxWidth: {
                'khg-half': '20rem',
                'khg-quarter3': '30rem',
                'khg-full': '40rem',
            },
            fontFamily: {
                'noto-sans': ['Noto Sans KR'],
            },
        },
    },
    plugins: [],
}
