# `commtikz`: A TikZ Library for Electro-Optical, Photonics, RF & Communications Schematics

`commtikz` is a modular LaTeX/TikZ library for drawing publication-quality block diagrams and experimental setup schematics for electro-optical, photonics, fiber-optic, RF, and digital signal processing (DSP) systems.

---

## Features

- **Native PGF/TikZ Node Shapes**: Every component is a native PGF shape with crisp mitered geometry that works directly with `\node[...]`, `positioning` (`right=of ...`), `chains`, `fit`, and coordinate calculations (`calc`).
- **Font-Matched Stroke Weight**: Default line width (`0.6pt`) is calibrated to match the visual stroke weight of standard 10pt-11pt LaTeX fonts, with one-key global or scoped customization (`commtikz line width=<dimen>` or `commtikz match font`).
- **Background-Layer Signal Connectors**: Signal paths (`opt`, `rf`, `optrf`, `dc`, `ctrl`) are automatically rendered on the `background` layer behind component shapes so connector wires never overlap across component interiors.
- **Dual Port & Compass Anchor System**:
  - **0-based multi-port anchors**: `W0..Wn`, `E0..En`, `N0..Nn`, `S0..Sn` (configurable per side via `numW`, `numE`, `numN`, `numS` or `ports={W=2, E=4, N=1, S=1}`), plus `in`, `out`, `1..4` (on `circulator`), and semantic ports (`sig`, `lo`, `I+`, `I-`, `Q+`, `Q-` on `hybrid90`; `rf`, `dc`, `rfdc` on `biastee`).
  - **Standard TikZ compass anchors**: `west` (`W`), `east` (`E`), `north` (`N`), `south` (`S`), `north east` (`NE`), `north west` (`NW`), `south east` (`SE`), `south west` (`SW`), `center`.
- **Signal-Domain Path Styles, Waveguide Bends & Inline Placement**:
  - Predefined signal domains: `opt` (`OPTcol`, `#1F77B4` blue), `rf` (`RFcol`, `#D62728` red), `optrf` (`OPTRFcol`, `#9467BD` purple), `dc` (`DCcol`), and `ctrl` (`CTRLcol`, dashed).
  - Mid-path and end-path arrows: `->-`, `-<-`, `->>-`, `-<<-`, `opt->`, `rf->`, `optrf->`.
  - Smooth Bezier connectors (`to[arcz]`, `to[arcn]`, `to[arc2]`, `to[arc3]`, `to[arcloop]`) and native rounded orthogonal turns (`waveguide bend`, `opt bend`).
  - Inline 2-port component placement along paths: `to[inline=...]`, `to[to fiber]`, `to[to voa]`, `to[to polctrl]`, `to[to fbg]`, `to[to isolator]`, `to[to pm]`, `to[to mzm]`, `to[to filter]`, `to[to amp]`.

---

## Installation

### Option 1: Local Project Directory
Copy all `.sty` and `.code.tex` files into your LaTeX project directory alongside your main `.tex` file.

### Option 2: User `TEXMFHOME` Tree (System-wide for your user)
Clone this repository into your local `texmf` directory so `commtikz` is available in any document:

```bash
mkdir -p "$(kpsewhich -var-value=TEXMFHOME)/tex/latex/commtikz"
cp commtikz.sty tikzlibrarycommtikz*.code.tex "$(kpsewhich -var-value=TEXMFHOME)/tex/latex/commtikz/"
```

Then load the library in your LaTeX preamble:

```latex
\usepackage{commtikz}
% or:
\usepackage{tikz}
\usetikzlibrary{commtikz}
```

---

## Quick Start

```latex
\documentclass{article}
\usepackage{commtikz}

\begin{document}
\begin{tikzpicture}[commtikz unit=0.85cm]
  \node[ld, label=above:{\footnotesize CW Laser}] (ld) at (0,0) {};
  \node[polctrl, right=0.8cm of ld, label=above:{\footnotesize PC}] (pc) {};
  \node[mzm, right=0.9cm of pc, numN=1] (mzm) {};
  \node[awg, above=1.2cm of mzm] (awg) {};
  \node[fiber, right=0.9cm of mzm, label=above:{\footnotesize SMF}] (smf) {};
  \node[pd, right=0.9cm of smf, label=above:{\footnotesize PD}] (pd) {};
  \node[esa, right=0.9cm of pd] (esa) {};

  \draw[opt, ->-] (ld.E0) -- (pc.W0);
  \draw[opt, ->-] (pc.E0) -- (mzm.W0);
  \draw[rf->]     (awg.S0) -- (mzm.N0);
  \draw[opt, ->-] (mzm.E0) -- (smf.W0);
  \draw[opt, ->-] (smf.E0) -- (pd.W0);
  \draw[rf, ->-]  (pd.E0) -- (esa.W0);
\end{tikzpicture}
\end{document}
```

---

## Usage Guide

### 1. What `commtikz unit` Controls & How to Scale Building Blocks or Whole Figures

#### What `commtikz unit` controls
`commtikz unit=<dimension>` (default `1cm`, with shorthand `commtikz scale=<factor>`) defines the base length unit $u$ used to compute the physical dimensions of all `commtikz` building blocks:
- Every component's dimensionless size keys—`width`, `height`, `height1`, `height2` (for `mux`/`demux`), and `comp radius` (for circular blocks)—as well as internal arrowheads (`voa`, `ld`, `isolator`, `phaseshifter`) are multiplied by `commtikz unit`.
- For example, at the default `commtikz unit=1cm`:
  - A $1\times1$ square block (`width=1, height=1`) measures $1.0\,\text{cm} \times 1.0\,\text{cm}$.
  - A circular block (`comp radius=0.5`) has radius $0.5\,\text{cm}$ (diameter $1.0\,\text{cm}$).
  - An MZM (`width=1.40, height=0.90`) measures $1.40\,\text{cm} \times 0.90\,\text{cm}$, and an IQ modulator (`width=2.05, height=1.10`) measures $2.05\,\text{cm} \times 1.10\,\text{cm}$.

#### Scaling a single building block
- **Uniform scaling (preserving aspect ratio)**: Pass `commtikz unit=<dimen>` or `commtikz scale=<factor>` on the node:
  ```latex
  \node[iqm, commtikz scale=0.75] (iqm) {};
  \node[hybrid90, commtikz unit=1.2cm] (hyb) {};
  ```
- **Independent width / height / radius**: Override `width`, `height` (`block width`, `block height`), `height1`/`height2`, or `comp radius` on the node (either as dimensionless multiples of `commtikz unit` or with explicit TeX units like `1.8cm`):
  ```latex
  \node[commrect, width=2.4, height=1.6] (dsp) {};
  \node[mux, width=1.2, height1=2.6, height2=1.0] (wdm) {};
  \node[circulator, comp radius=0.65] (circ) {};
  ```

#### Scaling the whole figure
- **Scale all building blocks while keeping text labels at normal font size**:
  ```latex
  % Scales all component shapes to 80% and coordinate grid (x,y) to 80%
  \begin{tikzpicture}[commtikz unit=0.8cm, x=0.8cm, y=0.8cm]
    ...
  \end{tikzpicture}
  ```
- **Scale only the building blocks (leaving coordinate positions unchanged)**:
  ```latex
  \begin{tikzpicture}[commtikz unit=0.8cm]
    ...
  \end{tikzpicture}
  ```
- **Scale the entire figure geometrically (including `positioning` distances and text)**:
  ```latex
  \begin{tikzpicture}[scale=0.8, every node/.style={transform shape}]
    ...
  \end{tikzpicture}
  ```

### 2. Adjusting Line Width to Match Your Font
By default, `commtikz` uses a stroke width of `0.6pt` (with `0.45pt` for inner instrument display traces), which visually matches 10pt-11pt Computer Modern / Latin Modern text. You can adjust the line width globally or per `tikzpicture`:

```latex
% Automatically scale line width to 0.055em of the active document font size
\begin{tikzpicture}[commtikz match font] ... \end{tikzpicture}

% Set an explicit line width (automatically scales inner traces to 75%)
\begin{tikzpicture}[commtikz line width=0.5pt] ... \end{tikzpicture}

% Or control block outlines, inner instrument traces, and signal wires independently
\tikzset{
  commtikz block line width=0.65pt,
  commtikz inner line width=0.45pt,
  commtikz signal line width=0.65pt,
}
```

### 3. Multi-Port Anchors & Port Alignment (`port span`)
Every rectangular and trapezoidal component supports configuring the number of ports on each side via `numW`, `numE`, `numN`, `numS` or `ports={W=..., E=..., N=..., S=...}`:

```latex
\node[commrect, width=2.4, height=1.8, ports={W=2, E=4, N=1, S=1}, comp label=DSP] (dsp) {};
\draw[opt->] (in0) -- (dsp.W0);
\draw[opt->] (in1) -- (dsp.W1);
\draw[rf->]  (dsp.E0) -- (out0);
```

To align multi-port spacing between two blocks of **different widths or heights** so their connecting lines are strictly perpendicular:
- **Method A (`port span x` / `port span y`)**: Set `port span x=<width>` (for `N`/`S` ports) or `port span y=<height>` (for `E`/`W` ports) so both blocks distribute their ports over the same span (by default, `iqm` sets `port span x=1.55` to match `awg`):
  ```latex
  \node[awg, numS=2] (awg) at (0, 1.8) {};
  \node[iqm, numN=2, port span x=1.55] (iqm) at (0, 0) {};
  \draw[rf->] (awg.S0) -- (iqm.N0); % strictly vertical
  \draw[rf->] (awg.S1) -- (iqm.N1); % strictly vertical
  ```
- **Method B (`to[perp]` / `to[vperp]` / `to[hperp]` or `|-` / `-|` coordinate projection)**: Project perpendicular to the target edge without needing matching port spans:
  ```latex
  \draw[rf->] (awg.S0) to[perp] (iqm.north); % or: (awg.S0) -- (awg.S0 |- iqm.north);
  \draw[rf->] (awg.S1) to[perp] (iqm.north);
  ```

### 4. Signal Connectors, Circular Bends (90°/180°) & Inline Components
The `bend=<radius>` (default `0.22cm`) and `uturn` / `uturn left` styles work with **all** connection types (`opt`, `rf`, `optrf`, `dc`, `ctrl`, or general paths). Convenience domain shorthands `opt bend`, `rf bend`, `optrf bend`, `dc bend`, and `ctrl bend` combine the domain style with `bend`:

```latex
% 90-degree circular bends on any connection type (opt, rf, optrf, dc, ctrl)
\draw[opt, bend=0.22cm, ->-=0.75] (a.E0) |- (b.W0);   % or \draw[opt bend=0.22cm, ...]
\draw[rf, bend=0.18cm, rf->]      (c.S0) |- (d.W0);   % or \draw[rf bend=0.18cm, ...]
\draw[dc bend=0.18cm, dc->]       (vdd)  -| (amp.N0);

% 180-degree semicircular U-turns (work on opt, rf, optrf, dc, ctrl)
\draw[opt, ->-] (a.E0) to[uturn] (b.E0);
\draw[rf, ->-]  (c.W0) to[uturn left] (d.W0);

% S-curve and arc Bezier connectors
\draw[opt, ->-] (a.E0) to[arcz] (b.W0);
\draw[rf, ->-]  (a.E0) to[arc2=25] (b.W0);

% Inline component placement along a path (fiberspool matches path color automatically)
\draw[opt] (0,0) to[to fiberspool={label=above:SMF}] (3,0)
                 to[to voa={label=above:VOA}] (6,0);
```

---

## Component Reference

### 1. Core Optical & System Building Blocks
- **Generic Blocks & Tap**: `commrect` (`rectblock`), `commsquare` (`squareblock`), `commcircle` (`circleblock`), `couplercirc` (`coupler`)
- **Passive & Free-Space Optics**: `bs` (`beamsplitter`), `pbs`, `mirror`, `polarizer`, `waveplate` (`hwp`, `qwp`), `fiberspool` (`fiber`, `smf`), `polctrl` (`pc`), `voa`, `fbg`, `circulator`, `isolator` (`iso`), `mux`, `demux`, `splitter`, `combiner`, `dcoupler`
- **Modulators, Sources & Detectors**: `pm` (`phasemod`), `mzm`, `iqm` (`dpmzm`), `ringmod` (`mrr`), `phaseshifter`, `ld` (`laser`), `pd` (`photodiode`), `bpd`, `hybrid90`, `edfa`, `soa`
- **Test & Measurement Instruments**: `osa`, `esa`, `awg`, `osc` (`scope`, `dso`)

### 2. RF, Analog & DSP Building Blocks
- **Filters**: `filter`, `lpf` (`response=lp`), `bpf` (`response=bp`, `obpf`), `hpf` (`response=hp`), `notchfilter` (`response=notch`)
- **Amplifiers & Conditioning**: `amp`, `vga`, `biastee`, `rfatt`, `termination` (`term`)
- **Data Converters, Mixers & Oscillators**: `adc`, `dac`, `mixer`, `sum`, `sumsigma`, `oscillator` (`lo`), `oscillatorbox`, `demod`

### 3. Electronic & Electrical Circuit Components (`commtikz.electrical`)
- **Passives**: `resistor` (`R`, `rbox`, `to resistor`, `to R`), `capacitor` (`C`, `to capacitor`, `to C`), `inductor` (`L`, `to inductor`, `to L`)
- **Diodes & Optoelectronics**: `diode` (`D`, `to diode`, `to D`), `zener` (`to zener`), `elpd` (`cktpd`, `to elpd`), `elld` (`led`, `to elld`)
- **Sources & Rails**: `vsource` (`dcvoltage`, `to vsource`), `isource` (`dccurrent`, `to isource`), `acsource` (`rfsource`, `to acsource`), `ground` (`gnd`), `vcc` (`vdd`), `edot` (`junction`)
- **Active Devices & Transistors**: `opamp` (`tia`), `nmos` (`fet`), `npn` (`bjt`)

---

## Repository Structure

| File | Description |
| :--- | :--- |
| [`commtikz.sty`](commtikz.sty) | LaTeX package wrapper (`\usepackage{commtikz}`) |
| [`tikzlibrarycommtikz.code.tex`](tikzlibrarycommtikz.code.tex) | Main TikZ library entrypoint (`\usetikzlibrary{commtikz}`) & color palette |
| [`tikzlibrarycommtikz.base.code.tex`](tikzlibrarycommtikz.base.code.tex) | PGF keys, line-width controls, dynamic multi-port anchor engine, and base block shapes (`commrect`, `commcircle`, `commsquare`) |
| [`tikzlibrarycommtikz.optical.code.tex`](tikzlibrarycommtikz.optical.code.tex) | Optical, fiber, and electro-optical PGF shapes (`mzm`, `iqm`, `pm`, `ld`, `pd`, `bpd`, `hybrid90`, `mux`, `circulator`, `fiberspool`, `polctrl`, `voa`, `fbg`, `bs`, `pbs`, `ringmod`, `phaseshifter`, etc.) |
| [`tikzlibrarycommtikz.instruments.code.tex`](tikzlibrarycommtikz.instruments.code.tex) | Lab instrument shapes with waveform/spectrum screens and control panel buttons (`osa`, `esa`, `awg`, `osc`/`scope`/`dso`) |
| [`tikzlibrarycommtikz.rf.code.tex`](tikzlibrarycommtikz.rf.code.tex) | RF, analog, and DSP shapes (`amp`, `vga`, `edfa`, `soa`, `filter`, `lpf`/`bpf`/`hpf`/`notchfilter`, `adc`, `dac`, `mixer`, `sum`, `sumsigma`, `oscillator`, `demod`, `biastee`, `rfatt`, `termination`) |
| [`tikzlibrarycommtikz.electrical.code.tex`](tikzlibrarycommtikz.electrical.code.tex) | Electronic and electrical circuit components (`resistor`, `capacitor`, `inductor`, `diode`, `zener`, `elpd`, `elld`, `vsource`, `isource`, `acsource`, `ground`, `vcc`, `opamp`/`tia`, `nmos`, `npn`) |
| [`tikzlibrarycommtikz.paths.code.tex`](tikzlibrarycommtikz.paths.code.tex) | Background-layer signal path styles, rounded waveguide bends (`opt bend`, `waveguide bend`, `uturn`), Bezier connectors, and `to[...]` inline path placement |
| [`commtikz-doc.tex`](commtikz-doc.tex) / [`commtikz-doc.pdf`](commtikz-doc.pdf) | Full visual component catalog and example electro-optical setup schematics |
| [`Makefile`](Makefile) | Build automation for `commtikz-doc.pdf` |

---

## Building the Documentation

Compile [`commtikz-doc.pdf`](commtikz-doc.pdf) using `pdflatex` (or `make doc`):

```bash
pdflatex commtikz-doc.tex
```

---

## License

Released under the [MIT License](LICENSE).
