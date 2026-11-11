# commtikz

A LaTeX/TikZ library for photonics, optical communications, RF, DSP, and
electronic circuit diagrams. Components are native PGF shapes with named
ports, configurable dimensions, and standard TikZ positioning support.

## Installation

Copy `commtikz.sty` and all `tikzlibrarycommtikz*.code.tex` files into your
LaTeX project, or install them in your user TeX tree:

```bash
mkdir -p "$(kpsewhich -var-value=TEXMFHOME)/tex/latex/commtikz"
cp commtikz.sty tikzlibrarycommtikz*.code.tex \
  "$(kpsewhich -var-value=TEXMFHOME)/tex/latex/commtikz/"
```

Load either the package or the TikZ library:

```latex
\usepackage{commtikz}
% Alternatively: \usepackage{tikz} \usetikzlibrary{commtikz}
```

## Quick start

```latex
\documentclass{article}
\usepackage{commtikz}

\begin{document}
\begin{tikzpicture}
  \node[ld, label=above:Laser] (laser) {};
  \node[mzm, right=8mm of laser] (mod) {};
  \node[awg, above=1cm of mod] (drive) {};
  \node[pd, right=3cm of mod, label=above:PD] (detector) {};
  \node[osc, right=8mm of detector] (scope) {};

  \draw[opt->] (laser.E0) -- (mod.W0);
  \draw[rf->] (drive.S0) -- (mod.N0);
  \draw[opt] (mod.E0) to[to fiberspool] (detector.W0);
  \draw[rf->] (detector.E0) -- (scope.W0);
\end{tikzpicture}
\end{document}
```

The [visual catalog](commtikz-doc.pdf) includes component drawings and complete
optical, coherent-receiver, and circuit examples.

## Components

| Category | Styles |
| --- | --- |
| Generic blocks | `commrect`, `commsquare`, `commcircle` |
| Fiber and passive optics | `coupler`, `fiberspool`, `polctrl`, `voa`, `fbg`, `circulator`, `isolator`, `mux`, `demux`, `splitter`, `combiner`, `dcoupler` |
| Free-space optics | `bs`, `pbs`, `mirror`, `polarizer`, `waveplate`, `hwp`, `qwp` |
| Modulators | `pm`, `mzm`, `iqm`, `ringmod`, `phaseshifter` |
| Optical sources and detectors | `ld`, `pd`, `bpd`, `hybrid90`, `edfa`, `soa` |
| Instruments | `osa`, `esa`, `awg`, `osc` |
| RF and signal processing | `filter`, `lpf`, `bpf`, `hpf`, `notchfilter`, `amp`, `vga`, `biastee`, `rfatt`, `adc`, `dac`, `mixer`, `sum`, `sumsigma`, `oscillator`, `oscillatorbox`, `demod`, `termination` |
| Circuit passives and diodes | `resistor`, `capacitor`, `inductor`, `diode`, `zener`, `elpd`, `elld` |
| Circuit sources and active devices | `vsource`, `isource`, `acsource`, `ground`, `vcc`, `edot`, `opamp`, `nmos`, `npn` |

Common aliases include `fiber`/`smf` for `fiberspool`, `pc` for `polctrl`,
`laser` for `ld`, `photodiode` for `pd`, `scope`/`dso` for `osc`, `dpmzm` for
`iqm`, `mrr` for `ringmod`, `R`/`C`/`L` for circuit passives, `led` for `elld`,
and `tia` for `opamp`.

## Dimensions and scaling

`commtikz unit` sets the base unit (default `1cm`). Dimensionless `width`,
`height`, and `comp radius` values multiply that unit and the class scale:

| Class | Scale key | Default |
| --- | --- | --- |
| Optical, RF, instrument, and generic blocks | `commtikz block scale` | `0.85` |
| Electrical circuit symbols | `commtikz circuit scale` | `1.10` |

For example, a `width=1, height=1` block measures 0.85×0.85 cm at the default
unit. Ordinary boxed components share these dimensions; modulators with
multiple paths, instruments, multi-channel receivers, and circuit symbols
have their own proportions.

```latex
\node[pm, commtikz scale=0.75] (mod) {};       % base unit = 0.75cm
\node[commrect, width=2, height=1.5] (dsp) {};
\node[commrect, width=2cm, height=1cm] (box) {}; % physical dimensions
\node[circulator, comp radius=0.65] (circ) {};
\node[mux, width=1.2, height1=2.6, height2=1] (mux) {};
```

Explicit dimensions such as `width=2cm` bypass the class scale. Use
`commtikz legacy sizes` to set both class scales to 1. Set dimensions after
the component style when overriding a node's defaults.

To scale component geometry and the coordinate grid together while retaining
normal text sizes:

```latex
\begin{tikzpicture}[commtikz unit=0.8cm, x=0.8cm, y=0.8cm]
  ...
\end{tikzpicture}
```

For geometric scaling of the entire drawing, including text and positioning
distances, use `scale=0.8, every node/.style={transform shape}`.

## Labels and line styles

Use TikZ's `label` option for external annotations. Component labels have a
default clearance of `3pt` from the symbol boundary. Optical-arrow bounds are
included for circuit photodiodes and LEDs, including rotated symbols.

```latex
\node[pd, label=above:Detector] (pd) {};
\node[elpd, rotate=90, transform shape, label=above:PD] (circuitpd) {};
\node[amp, commtikz label distance=5pt, label=above:Amplifier] (amp) {};
```

`commtikz label distance=<dimension>` sets the component clearance on a
picture, scope, or node. A label-specific override uses standard TikZ syntax:
`label={[label distance=1pt]above:Detector}`. Label directions follow the
component's rotation. Separately positioned text nodes use their own
positioning distances.

Default component and signal strokes are `0.6pt`; instrument traces are
`0.45pt`. Configure them together or independently:

```latex
\tikzset{
  commtikz line width=0.5pt,
  % Alternatively:
  % commtikz block line width=0.6pt,
  % commtikz inner line width=0.4pt,
  % commtikz signal line width=0.6pt,
}
```

`commtikz match font` sets the line width to `0.055em` of the current font.
Use `draw=<color>`, `text=<color>`, and `fillcol=<color>` to style components.
`comp label=<text>` supplies internal text on shapes that support it.

## Ports and connections

Components provide standard compass anchors (`west`, `east`, `north`,
`south`, corners, and `center`) and short aliases (`W`, `E`, `N`, `S`, etc.).
Numbered side ports use zero-based names: `W0`, `W1`, `E0`, and so on.

Generic blocks support configurable port counts and spacing:

```latex
\node[commrect, width=2.4, height=1.8,
      ports={W=2, E=4, N=1, S=1}, comp label=DSP] (dsp) {};
```

`numW`, `numE`, `numN`, and `numS` set counts individually. `port span x`
controls N/S spacing, `port span y` controls W/E spacing, and `port order`
selects `top to bottom` or `bottom to top` for W/E ports.

Components with fixed internal paths require these W/E counts:

| Styles | West count | East count |
| --- | --- | --- |
| `splitter` | 1 | 2 |
| `combiner` | 2 | 1 |
| `dcoupler` | 2 | 2 |
| `hybrid90` | 2 | 4 |
| `bpd`, `opamp` / `tia` | 2 | 1 |
| `pm`, `mzm`, `iqm`, `ringmod` | 1 | 1 |

These shapes require top-to-bottom port order and full-height W/E spacing;
incompatible settings or unavailable numbered ports raise a package error.
N/S control-port counts remain configurable.

Semantic anchors include:

- `sig`, `lo`, `I+`, `I-`, `Q+`, `Q-` on `hybrid90`.
- `rf`, `dc`, `rfdc` on `biastee`.
- `in-`, `in+`, `out` on `opamp`; `mirror flip` swaps input polarity.
- `G`, `D`, `S` on `nmos` and `B`, `C`, `E` on `npn`.
- `bus in`, `bus out` on `ringmod`; `drop in`, `drop out` require `add drop`.
- `1` (west), `2` (east), `3` (south), `4` (north) on `circulator`.

For example:

```latex
\node[ringmod, add drop] (ring) {};
\draw[opt] (-2,0) -- (ring.bus in);
\draw[opt] (ring.bus out) -- (2,0);
\draw[opt] (ring.drop out) -- ++(1,0);
```

### Signal paths and routing

| Style | Color |
| --- | --- |
| `opt` | `OPTcol` — blue |
| `rf` | `RFcol` — red |
| `optrf` | `OPTRFcol` — purple |
| `dc` | `DCcol` — green |
| `ctrl` | `CTRLcol` — gray, dashed |

Signal paths render behind component nodes. Add an endpoint arrow with
`opt->`, `rf->`, `optrf->`, `dc->`, or `ctrl->`; use `->-` / `-<-` for a
mid-path arrow and `->>-` / `-<<-` for paired mid-path arrows.

```latex
\draw[opt, ->-] (a.E0) to[arcz] (b.W0);       % smooth S-curve
\draw[rf, bend=2mm, ->-] (c.S0) |- (d.W0);   % rounded corner
\draw[opt] (a.E0) to[uturn] (b.E0);          % semicircular return
\draw[rf->] (drive.S0) to[perp] (mod.north); % perpendicular projection
```

Other routing helpers include `arcn`, `arc2`, `arc3`, `arcloop`, `uturn left`,
`hvh`, and `vhv`. `port span x=1.55` on IQM matches AWG's default N/S span
when both use the same unit and block scale.

### Inline components and colors

Place two-port components on straight paths using `to[inline={...}]` or a
shorthand:

```latex
\draw[opt] (0,0) to[to fiberspool={label=above:SMF}] (3,0)
                 to[to voa] (6,0);
\draw[rf] (0,-2) to[to R={label=above:$R$}] (3,-2);
\draw[optrf] (0,-4) to[to coupler] (3,-4);
```

Inline shorthands cover fiber spools, couplers, optical controllers and
modulators, filters, amplifiers, and circuit passives/diodes. They rotate the
component with the path; `inline upright={...}` retains its orientation.

Standalone couplers and fiber spools use the current drawing color (normally
black). Their inline shorthands inherit the connector color. An explicit
option such as `to coupler={draw=black}` overrides that color. Separately
placed nodes can be colored with `draw=<color>`.

## Documentation and validation

Build the [component catalog and examples](commtikz-doc.pdf) with `make doc`,
or compile `commtikz-doc.tex` twice with `pdflatex`.

Run `make check` or `python3 tests/check.py` for geometry, port, color, and
arrowhead checks. Visual sheets are written to
`/tmp/commtikz-check/components.pdf`.

The implementation is split into `base`, `optical`, `instruments`, `rf`,
`electrical`, and `paths` TikZ libraries, loaded by `commtikz.sty` or
`\usetikzlibrary{commtikz}`.

## License

[MIT](LICENSE).
