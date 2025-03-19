#!/usr/bin/env python3
import argparse
import os
import pandas as pd
import matplotlib.pyplot as plt
import holoviews as hv
from holoviews import opts
from bokeh.models import HoverTool
from bokeh.io import output_file as bokeh_output_file, save
hv.extension('bokeh')

def plot_matplotlib_cactus(csv_file, output_file, type):
    """Read data from the CSV file and generate a cactus plot using gnuplotlib."""
    df_raw = pd.read_csv(csv_file, index_col=0)
    # print(df_raw)

    df = df_raw.reset_index(drop=True).dropna(how='any')
    # print(df)
    df = df.apply(sorted, axis=0)
    # print(df)
    if len(df) == 0:
        print("No data to plot.")
        return

    obj_columns = [
        (f"mp-p-low-{type}", "MP-Low"),
        (f"mp-p-mid-{type}", "MP-Mid"),
        (f"mp-p-hi-{type}", "MP-High"),
        (f"mp-is-p-low-{type}", "MP+IS-Low"),
        (f"mp-is-p-mid-{type}", "MP+IS-Mid"),
        (f"mp-is-p-hi-{type}", "MP+IS-High"),
        (f"mp-is1-p-low-{type}", "MP+IS1-Low"),
        (f"mp-is1-p-mid-{type}", "MP+IS1-Mid"),
        (f"mp-is1-p-hi-{type}", "MP+IS1-High"),
        (f"mp-is10-p-low-{type}", "MP+IS10-Low"),
        (f"mp-is10-p-mid-{type}", "MP+IS10-Mid"),
        (f"mp-is10-p-hi-{type}", "MP+IS10-High"),
        (f"mp-is100-p-low-{type}", "MP+IS100-Low"),
        (f"mp-is100-p-mid-{type}", "MP+IS100-Mid"),
        (f"mp-is100-p-hi-{type}", "MP+IS100-High"),
        (f"mp-ps-p-low-{type}", "MP+PS-Low"),
        (f"mp-ps-p-mid-{type}", "MP+PS-Mid"),
        (f"mp-ps-p-hi-{type}", "MP+PS-High"),
        (f"lnps-10-{type}", "LNPS-10"),
        (f"lnps-30-{type}", "LNPS-30"),
        (f"lnps-60-{type}", "LNPS-60"),
        (f"ps-{type}", "PS"),
    ]

    size = 0
    for col in obj_columns:
        if col[0] in df.columns:
            size += 1

    # plt.figure(figsize=(10, 6))
    if size <= 15:
        plt.figure(figsize=(8*0.8, 6*0.8))
    else:
        plt.figure(figsize=(10*0.8, 6*0.8))

    line_styles = [
     (0, (3, 3)),       # dashed
     (0, (3, 2, 1, 2)), # densely dashdotted
     (0, (1, 1)),       # densely dotted
    ]
    colors = [
        '#d62728', '#ff9896', '#e15759',  # Red shades
        '#2ca02c', '#98df8a', '#60bd68',  # Green shades
        '#ff7f0e', '#ffbb78', '#ff9f50',  # Orange shades
        '#9467bd', '#c5b0d5', '#8c6bb1',  # Purple shades
        '#f1c40f', '#f7dc6f', '#d4ac0d',  # Yellow shades
        '#17becf', '#9adbe4', '#28a3c4',  # Cyan shades
        '#8c564b', '#c49c94', '#a67c52',  # Brown shades
        '#e377c2', '#f7b7d2', '#d655a5',  # Pink shades
        '#7f7f7f', '#b0b0b0', '#d9d9d9',  # Gray shades
    ]
    dark_colors = [
        '#801718', '#995b5a', '#873435',  # Dark Red shades
        '#1a601a', '#5b8653', '#3a713e',  # Dark Green shades
        '#994c08', '#997048', '#995f30',  # Dark Orange shades
        '#593e71', '#766a80', '#54406a',  # Dark Purple shades
        '#9a780a', '#7a5a07', '#624906',  # Dark Yellow shades
        '#117a88', '#0f5f6d', '#0d4955',  # Dark Cyan shades
        '#5d4037', '#4a322c', '#3a2823',  # Dark Brown shades
        '#9c0d38', '#7a0a2b', '#5d081f',  # Dark Pink shades
        '#4c4c4c', '#696969', '#333333',  # Dark Gray shades
    ]
    lnps_colors = [
        '#1f77b4', '#4a90e2', '#85c1e9',  # Blue shades
    ]
    lnps_dark_colors = [
        '#13476c', '#2c5688', '#50748c',  # Dark Blue shades
    ]
    markers = ['s', 'p', 'P', '+', 'x', 'X', 'o', 'v', '^', 'D', '*', 'H', '<', '>']
    # markers = ['s', 's', 's', '^', '^', '^', 'D', 'D', 'D', 'o', 'o', 'o']

    # Plot each '-obj' column with different line styles
    other_idx = 0
    lnps_idx = 0
    idx = 0
    for col in obj_columns:
        if col[0] not in df.columns:
            continue
        if "LNPS" in col[1]:
            line_style = line_styles[lnps_idx % len(line_styles)]
            color = lnps_colors[lnps_idx % len(colors)]
            dark_color = lnps_dark_colors[lnps_idx % len(dark_colors)]
            lnps_idx += 1
        else:
            line_style = line_styles[other_idx % len(line_styles)]
            color = colors[other_idx % len(colors)]
            dark_color = dark_colors[other_idx % len(dark_colors)]
            # idx = other_idx
            other_idx += 1
        marker = markers[idx % len(markers)]
        marker_size = 5
        plt.plot(range(1, len(df[col[0]]) + 1), df[col[0]], label=col[1], linestyle=line_style, color=color, marker=marker, markersize=marker_size, alpha=0.75, markeredgecolor=dark_color, markeredgewidth=0.05)
        idx += 1

    plt.xlabel("Instance")
    if type == "obj":
        #plt.ylabel("Objective Value")
        plt.ylabel("Penalty Score (Lower is Better)")
        #plt.yscale('log')
        #plt.ylim(0.0001, 10000)
        #plt.ylim(0, 10000)
    elif type == "diff":
        #plt.ylabel("Differences")
        plt.ylabel("Modification Rate (% of changed shifts)")
    elif type == "freq":
        plt.ylabel("Frequency")
    if size <= 15:
        plt.legend(loc='upper left', handlelength=4)
    else:
        plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.grid()

    plt.tight_layout()

    # Modify output filename to include type
    output_file = f"{output_file.rsplit('.', 1)[0]}-{type}.{output_file.rsplit('.', 1)[1]}"

    # Save as a vector format (e.g., SVG or PDF)
    plt.savefig(output_file, format=output_file.split('.')[-1])
    print(f"Saved plot to {output_file}")

markers = hv.Cycle([
    'asterisk', 'circle', 'circle_cross', 'circle_x',
    'cross', 'dash', 'diamond', 'diamond_cross', 'hex',
    'inverted_triangle', 'square', 'square_cross', 'square_x', 'triangle', 'x'])

def hide_hover_icon(plot, element):
    for tool in plot.state.toolbar.tools:
        if isinstance(tool, HoverTool):
            tool.visible = False  # Hoverツールのアイコンを非表示

def plot_holoviews_cactus(csv_file, output_file, type):
    df_raw = pd.read_csv(csv_file, index_col=0)

    obj_columns = [
        (f"mp-p-low-{type}", "MP-Low"),
        (f"mp-p-mid-{type}", "MP-Mid"),
        (f"mp-p-hi-{type}", "MP-High"),
        (f"mp-is-p-low-{type}", "MP+IS-Low"),
        (f"mp-is-p-mid-{type}", "MP+IS-Mid"),
        (f"mp-is-p-hi-{type}", "MP+IS-High"),
        (f"mp-is1-p-low-{type}", "MP+IS1-Low"),
        (f"mp-is1-p-mid-{type}", "MP+IS1-Mid"),
        (f"mp-is1-p-hi-{type}", "MP+IS1-High"),
        (f"mp-is10-p-low-{type}", "MP+IS10-Low"),
        (f"mp-is10-p-mid-{type}", "MP+IS10-Mid"),
        (f"mp-is10-p-hi-{type}", "MP+IS10-High"),
        (f"mp-is100-p-low-{type}", "MP+IS100-Low"),
        (f"mp-is100-p-mid-{type}", "MP+IS100-Mid"),
        (f"mp-is100-p-hi-{type}", "MP+IS100-High"),
        (f"mp-ps-p-low-{type}", "MP+PS-Low"),
        (f"mp-ps-p-mid-{type}", "MP+PS-Mid"),
        (f"mp-ps-p-hi-{type}", "MP+PS-High"),
        (f"lnps-10-{type}", "LNPS-10"),
        (f"lnps-30-{type}", "LNPS-30"),
        (f"lnps-60-{type}", "LNPS-60"),
        (f"ps-{type}", "PS"),
    ]

    df = df_raw.reset_index().rename(columns={"index": "Instance"})
    df['Instance'] = df['Instance'].apply(os.path.basename)

    plots = []
    for col_name, label in obj_columns:
        if col_name not in df.columns:
            continue
        tdf = df[["Instance", col_name]].sort_values(by=col_name)
        tdf.insert(0, 'No', range(1, len(tdf) + 1))
        #print(tdf)

        g = hv.Scatter(tdf,
                    vdims=[col_name, 'No', 'Instance'],
                    kdims=['No'],
                    label=col_name)
        plots.append(hv.Curve(g))
        plots.append(g)

    if type == "obj":
        ylabel = "Penalty Score (Lower is Better)"
    elif type == "diff":
        ylabel = "Modification Rate (% of changed shifts)"
    elif type == "freq":
        ylabel = "Frequency"

    graph = hv.Overlay(plots).opts(
        opts.Overlay(
            width=1000, height=600,
            ylabel=ylabel, xlabel='Instances',
            legend_position='right',
            show_legend=True,
        ),
        opts.Curve(
            line_width=1,#0.5,
            muted_alpha = 0.1,
            show_legend=True,
        ),
        opts.Scatter(
            tools=['hover'],
            default_tools=['pan'],
            show_legend=True,
            marker=markers,
            fill_alpha=0.0,
            size=8,
            line_width=1,#0.5,
            muted_alpha = 0.0,
            hooks=[hide_hover_icon],
            hover_mode='vline',
        ),
    )
    # Save plot
    if output_file is not None:
        output_path = f"{output_file.rsplit('.', 1)[0]}-{type}.html"
        bokeh_output_file(output_path)
        save(hv.render(graph))
        print(f"Saved plot to {output_path}")
    return graph

def plot_all_holoviews_cactus(csv_file, output_file):
    obj = plot_holoviews_cactus(csv_file, None, "obj")
    diff = plot_holoviews_cactus(csv_file, None, "diff")
    freq = plot_holoviews_cactus(csv_file, None, "freq")

    layout = (obj + diff + freq).opts(sync_legends=True).cols(1)
    if output_file is not None:
        output_path = f"{output_file.rsplit('.', 1)[0]}.html"
        bokeh_output_file(output_path)
        save(hv.render(layout))
        print(f"Saved plot to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Plot a cactus plot from a CSV file using gnuplotlib.")
    parser.add_argument("csv_file", type=str, help="Path to the input CSV file")
    parser.add_argument("output_file", type=str, help="Path to save the output vector file (e.g., output.svg or output.pdf)")
    args = parser.parse_args()

    plot_matplotlib_cactus(args.csv_file, args.output_file, "obj")
    plot_matplotlib_cactus(args.csv_file, args.output_file, "diff")
    plot_matplotlib_cactus(args.csv_file, args.output_file, "freq")

    plot_all_holoviews_cactus(args.csv_file, args.output_file)

if __name__ == "__main__":
    main()

