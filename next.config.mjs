/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        hostname: "stsci-opo.org",
        protocol: "https",
        port: "",
      },
    ],
  },
};

export default nextConfig;
