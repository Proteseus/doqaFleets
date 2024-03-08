/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./*.{html,js}", "./!(build|dist|.*)/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        white: "#fff",
        "foundation-white-normal-hover": "#dbdbdb",
        "foundation-grey-light": "#e9e9e9",
        "foundation-yellow-light-active": "#faf3d0",
        "foundation-yellow-normal-active": "#bead53",
        "foundation-green-light": "#edf5f3",
        "foundation-green-light-active": "#C6E0DA",
        "foundation-green-normal": "#469b88",
        "foundation-green-normal-hover": "#3F8C7A",
        "foundation-green-dark": "#357466",
        "foundation-green-dark-hover": "#2A5D52",
        "foundation-blue-light": "#ebf2fa",
        "foundation-blue-normal": "#377cc8",
        "foundation-white-dark-active": "#6d6d6d",
        "foundation-grey-normal": "#242424",
        "gray-500": "#6b7280",
        "gray-900": "#111928",
        "gray-900-transparent": "#11192844",
        "foundation-white-normal": "#f3f3f3",
        "foundation-white-normal-active": "#c2c2c2",
        "gray-200": "#e5e7eb",
        "gray-50": "#f9fafb",
        "gray-300": "#d1d5db",
        "foundation-red-light": "#fceeec",
        "foundation-yellow-light": "#fdfbf0",
        "foundation-white-light": "#fefefe",
        "light-black": "#11263c",
        "foundation-white-light-hover": "#FDFDFD",
        "foundation-white-light-active": "#fbfbfb",
        "foundation-green-light-active": "#c6e0da",
        "foundatoin-grey-light": "#E9E9E9",
        "foundation-grey-light-active": "#bbbbbb",
        "foundation-red-light-active": "#F5CAC3",
        "foundation-red-normal": "#e0533d",
        "foundation-red-normal-hover": "#CA4B37",
        "foundation-white-dark-hover": "#929292",
      },
      spacing: {
        boundvariablesdata1: "16px",
        boundvariablesdata2: "8px",
        boundvariablesdata3: "2px",
        boundvariablesdata4: "10px",
        boundvariablesdata5: "8px",
        boundvariablesdata6: "24px",
        boundvariablesdata8: "12px",
        boundvariablesdata9: "20px",
      },
      fontFamily: {
        "satoshi-body-small": "Satoshi",
        "text-xs-font-normal": "Inter",
        "space-grostek-subheadline": "'Space Grotesk'",
      },
      borderRadius: {
        lg: "18px",
        mini: "15px",
        "10xs": "3px",
        boundvariablesdata7: "16px",
        "rounded-lg": "8px",
      },
    },
    fontSize: {
      base: "1rem",
      xs: "0.75rem",
      sm: "0.875rem",
      "7xl": "1.625rem",
      "13xl": "2rem",
      "5xl": "1.5rem",
      "3xs": "0.625rem",
      xl: "1.25rem",
      inherit: "inherit",
    },
  },
  corePlugins: {
    preflight: false,
  },
};
