#!/usr/bin/env python3
"""Prépare la photo pour la conversion ASCII.

1. Détourage du sujet (rembg si installé, sinon GrabCut OpenCV)
2. Contraste local (CLAHE) pour donner du relief au visage
3. Composition sur fond blanc pur (fond -> espaces dans l'ASCII)

Usage : python scripts/prep_photo.py source-photo.png
Sortie : source-prepped.png (niveaux de gris)
"""
import sys
import cv2
import numpy as np


def subject_mask(bgr):
    h, w = bgr.shape[:2]
    try:
        from rembg import remove  # type: ignore
        rgba = remove(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
        return (np.asarray(rgba)[:, :, 3] > 128).astype(np.uint8) * 255
    except Exception:
        pass

    # Fallback GrabCut : on initialise avec un rectangle + une zone sûre
    mask = np.full((h, w), cv2.GC_BGD, np.uint8)
    rect = (int(w * 0.10), int(h * 0.06), int(w * 0.80), int(h * 0.94))
    x, y, rw, rh = rect
    mask[y:y + rh, x:x + rw] = cv2.GC_PR_BGD
    # Tête + buste : probablement sujet
    cv2.ellipse(mask, (int(w * 0.50), int(h * 0.40)), (int(w * 0.24), int(h * 0.34)),
                0, 0, 360, cv2.GC_PR_FGD, -1)
    mask[int(h * 0.78):, int(w * 0.05):int(w * 0.95)] = cv2.GC_PR_FGD
    # Cœur du visage / pull : sujet certain
    cv2.ellipse(mask, (int(w * 0.50), int(h * 0.44)), (int(w * 0.13), int(h * 0.20)),
                0, 0, 360, cv2.GC_FGD, -1)
    mask[int(h * 0.92):, int(w * 0.25):int(w * 0.75)] = cv2.GC_FGD

    bgd = np.zeros((1, 65), np.float64)
    fgd = np.zeros((1, 65), np.float64)
    cv2.grabCut(bgr, mask, None, bgd, fgd, 8, cv2.GC_INIT_WITH_MASK)
    out = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    # Nettoyage morphologique + plus grande composante
    out = cv2.morphologyEx(out, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    out = cv2.morphologyEx(out, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    n, lab, stats, _ = cv2.connectedComponentsWithStats(out)
    if n > 1:
        biggest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
        out = np.where(lab == biggest, 255, 0).astype(np.uint8)
    return out


def main(src, dst="source-prepped.png"):
    bgr = cv2.imread(src)
    if bgr is None:
        sys.exit(f"Image introuvable : {src}")

    mask = subject_mask(bgr)
    # Retire les résidus de décor autour de la tête (au-dessus des épaules)
    h, w = mask.shape
    mask[: int(h * 0.70), : int(w * 0.275)] = 0
    mask[: int(h * 0.70), int(w * 0.75):] = 0
    soft = cv2.GaussianBlur(mask, (0, 0), 2.0).astype(np.float32) / 255.0

    gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.2, tileGridSize=(8, 8))
    gray = clahe.apply(gray)
    # Léger étirement de contraste sur le sujet uniquement
    subj = gray[mask > 0]
    lo, hi = np.percentile(subj, [2, 98])
    gray = np.clip((gray.astype(np.float32) - lo) / max(hi - lo, 1) * 255, 0, 255)

    # Sorties intermédiaires utilisées par le portrait en points (halftone)
    cv2.imwrite("source-gray.png", gray.astype(np.uint8))
    cv2.imwrite("source-mask.png", (soft * 255).astype(np.uint8))

    white = np.full_like(gray, 255.0)
    comp = gray * soft + white * (1.0 - soft)
    cv2.imwrite(dst, comp.astype(np.uint8))
    print(f"OK -> {dst}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "source-photo.png")
