module.exports = async (phase, { defaultConfig }) => {
    /**
     * @type {import('next').NextConfig}
     */
    const nextConfig = {
        reactStrictMode: true,
        images: {
            remotePatterns: [
            ],
        },
    }
    return nextConfig
}