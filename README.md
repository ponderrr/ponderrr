<div align="center" style="display:flex; flex-direction:column; gap:14px; align-items:center;">
  <!-- Pulsing text (SVG animate is allowed on GitHub; <style> tags are stripped) -->
  <svg width="240" height="60" viewBox="0 0 240 60" aria-label="I like ai.">
    <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"
      fill="#ffffff" font-family="Inter, system-ui, -apple-system, sans-serif" font-size="26" font-weight="600">
      I like ai.
      <animate attributeName="opacity" dur="2.8s" values="0.6;1;0.6" repeatCount="indefinite"/>
    </text>
  </svg>

  <!-- Single flowing wave (no external assets) -->
  <svg width="100%" height="190" viewBox="0 0 1200 190" preserveAspectRatio="none" style="border-radius:48px; overflow:hidden;">
    <defs>
      <linearGradient id="waveGrad" x1="0%" y1="0%" x2="0%" y2="100%">
        <stop offset="0%" stop-color="#00d9ff" />
        <stop offset="100%" stop-color="#8b5cf6" />
      </linearGradient>
      <clipPath id="waveClip">
        <rect x="0" y="0" width="1200" height="190" rx="48" ry="48" />
      </clipPath>
    </defs>

    <g clip-path="url(#waveClip)">
      <path fill="url(#waveGrad)" fill-opacity="0.85">
        <animate attributeName="d" dur="6.5s" repeatCount="indefinite"
          values="
            M-360,118 C220,8 620,178 1560,72 L1560,250 L-360,250 Z;
            M-360,40 C340,180 620,-22 1560,165 L1560,250 L-360,250 Z;
            M-360,132 C200,68 610,198 1560,30 L1560,250 L-360,250 Z;
            M-360,68 C340,-12 590,156 1560,140 L1560,250 L-360,250 Z;
            M-360,126 C230,14 605,194 1560,50 L1560,250 L-360,250 Z;
            M-360,118 C220,8 620,178 1560,72 L1560,250 L-360,250 Z" />

        <animateTransform attributeName="transform" attributeType="XML" type="translate"
          dur="9.5s" repeatCount="indefinite" values="0 0; -120 4; 0 -4; 60 2; 0 0" />
        <animateTransform attributeName="transform" attributeType="XML" additive="sum" type="skewX"
          dur="10.5s" repeatCount="indefinite" values="0; 6; -5; 2; 0" />
      </path>

      <animate xlink:href="#waveGrad" attributeName="x1" dur="10s" values="0%; 30%; 0%" repeatCount="indefinite" />
      <animate xlink:href="#waveGrad" attributeName="x2" dur="10s" values="0%; 90%; 0%" repeatCount="indefinite" />
    </g>
  </svg>

  <div style="padding-top:18px; width:100%; max-width:960px; display:grid; grid-template-columns:repeat(4, minmax(0,1fr)); gap:10px; justify-items:center;">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
    <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
    <img src="https://img.shields.io/badge/TensorFlow-FF6F00?style=for-the-badge&logo=tensorflow&logoColor=white" />
    <img src="https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" />

    <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" />
    <img src="https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white" />
    <img src="https://img.shields.io/badge/Polars-CD792C?style=for-the-badge&logo=polars&logoColor=white" />
    <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" />

    <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" />
    <img src="https://img.shields.io/badge/Azure-0078D4?style=for-the-badge&logo=microsoftazure&logoColor=white" />
    <img src="https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white" />
    <img src="https://img.shields.io/badge/C++-00599C?style=for-the-badge&logo=cplusplus&logoColor=white" />

    <img src="https://img.shields.io/badge/Cursor-000000?style=for-the-badge&logo=cursor&logoColor=white" />
    <a href="https://www.linkedin.com/in/robertponder/"><img src="https://img.shields.io/badge/LinkedIn-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" /></a>
    <a href="https://andrewponder.com"><img src="https://img.shields.io/badge/Portfolio-FF006E?style=for-the-badge&logo=safari&logoColor=white" /></a>
    <a href="mailto:andrew.ponderrr@icloud.com"><img src="https://img.shields.io/badge/Email-8B5CF6?style=for-the-badge&logo=gmail&logoColor=white" /></a>
  </div>
</div>
