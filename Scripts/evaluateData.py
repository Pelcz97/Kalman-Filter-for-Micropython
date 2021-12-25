import numpy as np
import matplotlib.pyplot as plt

def loadData():
    with open("data.txt", "r") as data_file:
        tags = data_file.readline()
        measurements = []
        filtered_measurements = []
        for i,line in enumerate(data_file):
            if i % 2 == 0:
                measurements.append(line.split())
            else:
                filtered_measurements.append(line.split())
    return tags, np.array(measurements).astype(float), np.array(filtered_measurements).astype(float)

def camera_to_screen_transform(data_in):
    transformation_matrix = np.array([[138, 22, 21],[ 35, 83, 36],[ 0, 0, 1]])
    data_in[2] = 1
    transformed_data =  np.linalg.inv(transformation_matrix) @ data_in.T
    return transformed_data

def main():
    tags, measurements, filtered_measurements = loadData()
    for i in range(len(filtered_measurements)):
        measurement = measurements[i]
        filtered_measurement = filtered_measurements[i]
        print(camera_to_screen_transform(measurement))

    """    koord_distances = (measurements[..., 0] - filtered_measurements[..., 0]) **2 + (measurements[..., 1] - filtered_measurements[..., 1]) **2
    rad_distances = (measurements[..., 2] - filtered_measurements[...,2]) **2
    fig, axs = plt.subplots(3)
    fig.suptitle('Koordinates & Radius')
    axs[0].plot(measurements[...,0])
    axs[0].plot(filtered_measurements[...,0])
    axs[0].set_title("x-Achse")
    axs[1].plot(measurements[...,1])
    axs[1].plot(filtered_measurements[...,1])
    axs[1].set_title("y-Achse")
    axs[2].plot(measurements[...,2])
    axs[2].plot(filtered_measurements[...,2])
    axs[2].set_title("Radius")

    for ax in axs.flat:
        ax.label_outer()
    plt.savefig("Plots/Koordinates_Radius.png")

    fig, axs = plt.subplots(2)
    fig.suptitle('Koordinates & Radius Differences')
    axs[0].plot(koord_distances)
    axs[0].set_title("Koordinate Difference")
    axs[1].plot(rad_distances)
    axs[1].set_title("Radius Difference")

    for ax in axs.flat:
        ax.label_outer()
    plt.savefig("Plots/Differences.png")

    fig, axs = plt.subplots(3)
    fig.suptitle('Koordinates & Radius Measurements')
    axs[0].plot(measurements[...,0])
    axs[0].set_title("x-Achse")
    axs[1].plot(measurements[...,1])
    axs[1].set_title("y-Achse")
    axs[2].plot(measurements[...,2])
    axs[2].set_title("Radius")

    for ax in axs.flat:
        ax.label_outer()
    plt.savefig("Plots/Measurement.png")

    fig, axs = plt.subplots(3)
    fig.suptitle('Koordinates & Radius Filtered Measurements')
    axs[0].plot(filtered_measurements[...,0])
    axs[0].set_title("x-Achse")
    axs[1].plot(filtered_measurements[...,1])
    axs[1].set_title("y-Achse")
    axs[2].plot(filtered_measurements[...,2])
    axs[2].set_title("Radius")

    for ax in axs.flat:
        ax.label_outer()
    plt.savefig("Plots/Filtered_Measurement.png")"""
    

    


if __name__ == "__main__":
    main()